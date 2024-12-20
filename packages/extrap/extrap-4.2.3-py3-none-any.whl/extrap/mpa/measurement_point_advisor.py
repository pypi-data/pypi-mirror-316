# This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)
#
# Copyright (c) 2020-2024, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of a BSD-style license.
# See the LICENSE file in the base directory for details.

import numbers
from collections.abc import Sequence
from typing import Union

from extrap.entities.coordinate import Coordinate
from extrap.entities.scaling_type import ScalingType
from extrap.mpa.add_selection_strategy import suggest_points_add_mode
from extrap.mpa.base_selection_strategy import suggest_points_base_mode
from extrap.mpa.gpr_selection_strategy import suggest_points_gpr_mode
from extrap.mpa.util import identify_selection_mode, build_parameter_value_series, identify_step_factor, \
    extend_parameter_value_series, get_search_space_generator, identify_possible_points, experiment_has_repetitions
from extrap.util.exceptions import RecoverableError
from extrap.util.progress_bar import DUMMY_PROGRESS


class MeasurementPointAdvisor:

    def __init__(self, budget, process_parameter_id, experiment, manual_pms_selection, manual_parameter_value_series,
                 calculate_cost_manual, number_processes, model_generator) -> None:

        self.budget = budget
        # print("budget:",budget)

        self.process_parameter_id = process_parameter_id
        # print("processes:",processes)

        self.experiment = experiment

        self.normalization = True

        self.manual_pms_selection = manual_pms_selection

        self.manual_parameter_value_series = manual_parameter_value_series

        self.calculate_cost_manual = calculate_cost_manual

        self.number_processes = number_processes

        self.model_generator = model_generator

        # set the minimum number of points required for modeling per direction with the sparse modeler
        self.min_points = 5

        # print("DEBUG selection_mode:",self.selection_mode)

    def calculate_current_cost(self, selected_callpaths, metric):
        if not experiment_has_repetitions(self.experiment):
            raise ValueError(f'Experiment has no measurements with repetitions.')
        core_time_total = 0
        measurements = self.experiment.measurements
        for callpath in selected_callpaths:
            core_time_callpath = 0
            for measurement in measurements[(callpath, metric)]:
                core_time_per_point = self.calculate_cost(measurement.coordinate,
                                                          measurement.mean) * measurement.repetitions
                core_time_callpath += core_time_per_point
            core_time_total += core_time_callpath

        return core_time_total

    def calculate_cost(self, point: Union[Sequence, Coordinate], runtime: numbers.Real) -> numbers.Real:
        if self.experiment.scaling == ScalingType.STRONG:
            return runtime
        if self.calculate_cost_manual:
            nr_processes = self.number_processes
        else:
            nr_processes = point[self.process_parameter_id]
        cost = runtime * nr_processes
        return cost

    def suggest_points(self, selected_callpaths, metric, pbar=DUMMY_PROGRESS):
        # identify the state of the selection process
        # possible states are:
        # 1. not enough points for modeling
        #   -> continue row of parameter values for all parameters until modeling requirements are reached
        # 2. enough points for modeling, without an additional point not part of the lines
        #   -> suggest an extra point not part of the lines for each parameter
        # 3. enough points for modeling with an additional point not part of the lines
        #   -> suggest additional points using the gpr method

        # can be: gpr, add, base
        # gpr -> suggest additional measurement points with the gpr method
        # add -> suggest an additional point that is not part of the lines for each parameter
        # base -> suggest points to complete the lines of points for each parameter
        selection_mode = identify_selection_mode(self.experiment, self.min_points)

        if not experiment_has_repetitions(self.experiment):
            raise ValueError(f'Experiment has no measurements with repetitions.')
        if self.manual_pms_selection:
            # 1.2.3. build the parameter series from manual entries in GUI

            parameter_value_series = []
            for i in range(len(self.experiment.parameters)):
                try:
                    value_series = self.manual_parameter_value_series[i].split(",")
                    y = []
                    for x in value_series:
                        x = x.strip()
                        if x:
                            y.append(float(x))
                    parameter_value_series.append(y)
                except ValueError as e:
                    raise RecoverableError(f'The value series "{self.manual_parameter_value_series[i]}" for '
                                           f'parameter {i} can not be parsed.') from e

        else:
            # 1. build a value series for each parameter
            parameter_value_series = build_parameter_value_series(self.experiment.coordinates)

            # 2. identify the step factor size for each parameter
            mean_step_size_factors = identify_step_factor(parameter_value_series)

            # 3. continue and complete these series for each parameter
            parameter_value_series = extend_parameter_value_series(parameter_value_series, mean_step_size_factors)

        # 4. create search space (1D, 2D, 3D, ND) from the series values of each parameter
        search_space_generator = get_search_space_generator(parameter_value_series)

        # 5. remove existing points from search space to obtain only new possible points
        possible_points = identify_possible_points(search_space_generator, self.experiment.coordinates)

        # if no callpath is selected use all call paths
        if len(selected_callpaths) == 0:
            selected_callpaths = self.experiment.callpaths

        # 6. suggest points using selected mode
        # a. base mode
        # a.1 choose the smallest of the values for each parameter
        # a.2 combine these values of each parameter to a coordinate
        # a.3 repeat until enough suggestions for cords to complete a line of 5 points for each parameter
        if selection_mode == "base":
            suggested_cords = suggest_points_base_mode(self.experiment,
                                                       parameter_value_series)
            return suggested_cords, None

        # 6. suggest points using add mode
        # b. add mode
        # b.1 predict the runtime of the possible_points using the existing performance models
        # b.2 calculate the cost of these points using the runtime (same calculation as for the current cost in the GUI)
        # b.3 choose the point from the seach space with the lowest cost
        # b.4 check if that point fits into the available budget
        # b.41 create a coordinate from it and suggest it if fits into budget
        # b.42 if not fit then need to show message instead that available budget is not sufficient and needs to be
        #      increased...
        elif selection_mode == "add":
            current_cost = self.calculate_current_cost(selected_callpaths, metric)
            suggested_cords = suggest_points_add_mode(self.experiment,
                                                      possible_points,
                                                      selected_callpaths,
                                                      metric,
                                                      self.calculate_cost,
                                                      self.budget,
                                                      current_cost,
                                                      self.model_generator)
            return suggested_cords, None

        # 6. suggest points using gpr mode
        # c. gpr mode
        # c.1 predict the runtime of these points using the existing performance models (only possible if already enough
        #     points existing for modeling)
        # c.2 calculate the cost of these points using the runtime (same calculation as for the current cost in the GUI)
        # c.3 all of the data is used as input to the GPR method
        # c.4 get the top x points suggested by the GPR method that do fit into the available budget
        # c.5 create coordinates and suggest them
        elif selection_mode == "gpr":
            current_cost = self.calculate_current_cost(selected_callpaths, metric)
            suggested_cords, rep_numbers = suggest_points_gpr_mode(self.experiment,
                                                                   possible_points,
                                                                   selected_callpaths,
                                                                   metric,
                                                                   self.calculate_cost,
                                                                   self.budget,
                                                                   current_cost,
                                                                   self.model_generator,
                                                                   pbar)
            return suggested_cords, rep_numbers
        else:
            raise ValueError("Invalid selection mode")

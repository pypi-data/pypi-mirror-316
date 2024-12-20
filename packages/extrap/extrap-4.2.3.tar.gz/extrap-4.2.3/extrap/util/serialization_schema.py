# This file is part of the Extra-P software (http://www.scalasca.org/software/extra-p)
#
# Copyright (c) 2020-2024, Technical University of Darmstadt, Germany
#
# This software may be modified and distributed under the terms of a BSD-style license.
# See the LICENSE file in the base directory for details.

import collections
import math
import typing
from abc import abstractmethod, ABC
from collections.abc import Mapping
from typing import Union, Sequence, Tuple, Type

import marshmallow
from marshmallow import post_load, fields, ValidationError, EXCLUDE
from marshmallow.base import SchemaABC
from marshmallow.fields import Field
from marshmallow.schema import Schema as _Schema

from extrap.entities.fraction import Fraction


class SchemaMeta(type(_Schema), type(ABC)):
    pass


class Schema(_Schema, ABC, metaclass=SchemaMeta):
    class Meta:
        ordered = True
        unknown = EXCLUDE

    @abstractmethod
    def create_object(self) -> Union[object, Tuple[type(NotImplemented), Type]]:
        raise NotImplementedError()

    def postprocess_object(self, obj: object) -> object:
        return obj

    def preprocess_object_data(self, data):
        return data

    @post_load
    def unpack_to_object(self, data, **kwargs):
        data = self.preprocess_object_data(data)
        obj = self.create_object()
        try:
            for k, v in data.items():
                setattr(obj, k, v)
        except AttributeError as e:
            print(e)
        return self.postprocess_object(obj)


class BaseSchema(Schema):
    _subclasses = None
    type_field = '$type'

    def create_object(self):
        raise NotImplementedError(f"{type(self)} has no create object method.")

    def __init_subclass__(cls, **kwargs):
        if not cls.__is_direct_subclass(cls, BaseSchema):
            obj = cls().create_object()
            if isinstance(obj, tuple) and obj[0] == NotImplemented:
                cls._subclasses[obj[1].__name__] = cls
            else:
                cls._subclasses[type(cls().create_object()).__name__] = cls
        else:
            cls._subclasses = {}
        super().__init_subclass__(**kwargs)

    @staticmethod
    def __is_direct_subclass(subclass, classs_):
        return subclass.mro()[1] == classs_

    def on_missing_sub_schema(self, type_, data, **kwargs):
        """Handles missing subschema. May return a parsed object to fail gracefully."""
        raise ValidationError(f'No subschema found for {type_} in {type(self).__name__}')

    def load(self, data, **kwargs):
        if self.__is_direct_subclass(type(self), BaseSchema) and self.type_field in data:
            type_ = data[self.type_field]
            del data[self.type_field]
            try:
                schema = self._subclasses[type_]()
            except KeyError:
                return self.on_missing_sub_schema(type, data, **kwargs)
            return schema.load(data, **kwargs)
        else:
            return super(BaseSchema, self).load(data, **kwargs)

    def dump(self, obj, **kwargs):
        if self.__is_direct_subclass(type(self), BaseSchema) and type(obj).__name__ in self._subclasses:
            return self._subclasses[type(obj).__name__]().dump(obj, **kwargs)
        else:
            result = super(BaseSchema, self).dump(obj, **kwargs)
            if type(obj).__name__ in self._subclasses:
                result[self.type_field] = type(obj).__name__
            return result


def make_value_schema(class_, value):
    class Schema(_Schema):
        def dump(self, obj, *, many: bool = None):
            return getattr(obj, value)

        def load(self, data, *, many: bool = None, partial=None, unknown: str = None):
            return class_(data)

    return Schema


class TupleKeyDict(fields.Mapping):
    mapping_type = dict

    def __init__(self,
                 keys: Sequence[Union[Field, type]],
                 values: Union[Field, type] = None,
                 **kwargs):
        super(TupleKeyDict, self).__init__(fields.Tuple(keys), values, **kwargs)

    # noinspection PyProtectedMember
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None

        # Serialize keys
        keys = {
            k: self.key_field._serialize(k, None, None, **kwargs)
            for k in value.keys()
        }

        # Serialize values
        result = self.mapping_type()
        if self.value_field is None:
            for mk, v in value.items():
                curr_dict = result
                for k in keys[mk][:-1]:
                    if k not in curr_dict:
                        curr_dict[k] = self.mapping_type()
                    curr_dict = curr_dict[k]
                curr_dict[keys[mk][-1]] = v
        else:
            for mk, v in value.items():
                curr_dict = result
                for k in keys[mk][:-1]:
                    if k not in curr_dict:
                        curr_dict[k] = self.mapping_type()
                    curr_dict = curr_dict[k]
                curr_dict[keys[mk][-1]] = self.value_field._serialize(v, None, None, **kwargs)

        return result

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, Mapping):
            raise self.make_error("invalid")

        errors = collections.defaultdict(dict)

        def flatten(d, agg, parent_key, k_fields):
            field, *k_fields = k_fields
            if not isinstance(d, dict):
                raise ValidationError(f'Expected dict found: {d}')
            for key, v in d.items():
                try:
                    new_key = parent_key + [field.deserialize(key, **kwargs)]
                    if k_fields:
                        flatten(v, agg, new_key, k_fields)
                    else:
                        agg[tuple(new_key)] = v
                except ValidationError as error:
                    errors[key]["key"] = error.messages
            return agg

        value_dict = flatten(value, self.mapping_type(), [], list(self.key_field.tuple_fields))

        # Deserialize values
        result = self.mapping_type()
        if self.value_field is None:
            for key, val in value_dict.items():
                result[key] = val
        else:
            for key, val in value_dict.items():
                try:
                    deser_val = self.value_field.deserialize(val, **kwargs)
                except ValidationError as error:
                    errors[key]["value"] = error.messages
                    if error.valid_data is not None:
                        result[key] = error.valid_data
                else:
                    result[key] = deser_val

        if errors:
            raise ValidationError(errors, valid_data=result)

        return result


class NumberField(fields.Number):

    def _format_num(self, value):
        """Return the number value for value, given this field's `num_type`."""
        if not isinstance(value, str):
            return super()._format_num(value)
        elif value.lower() in ['nan', 'inf', '-inf']:
            return float(value)
        elif '/' in value:
            return Fraction(value)
        else:
            return super()._format_num(value)

    def _serialize(self, value, attr, obj, **kwargs):
        """Return a string if `self.as_string=True`, otherwise return this field's `num_type`."""
        if value is None:
            return None
        elif isinstance(value, Fraction):
            return self._to_string(value)
        elif math.isnan(value) or math.isinf(value):
            return self._to_string(value)
        else:
            ret = super()._format_num(value)
        return self._to_string(ret) if self.as_string else ret


class ListToMappingField(fields.List):
    def __init__(self, nested: typing.Union[SchemaABC, type, str, typing.Callable[[], SchemaABC]], key_field: str, *,
                 list_type=list, dump_condition=None, **kwargs):
        super().__init__(fields.Nested(nested), **kwargs)
        self.dump_condition = dump_condition
        self.list_type = list_type
        only_field = self.inner.schema.fields[key_field]
        self.key_field_name = only_field.data_key or key_field
        self.inner: fields.Nested

    def _serialize(self, value: typing.Any, attr: str, obj: typing.Any, **kwargs):
        if value is None:
            return None
        if self.dump_condition:
            value = [v for v in value if self.dump_condition(v)]
        value = super()._serialize(value, attr, obj, **kwargs)
        result = {}
        for each in value:
            key = each[self.key_field_name]
            del each[self.key_field_name]
            result[key] = each
        return result

    def _deserialize(self, value: typing.Any, attr: str, data: typing.Optional[typing.Mapping[str, typing.Any]],
                     **kwargs) -> typing.List[typing.Any]:
        if not isinstance(value, Mapping):
            raise self.make_error("invalid")

        value_list = []
        for k, v in value.items():
            if not isinstance(v, typing.MutableMapping):
                raise self.make_error("invalid")
            v[self.key_field_name] = k
            value_list.append(v)

        result = super()._deserialize(value_list, attr, data, **kwargs)

        if self.list_type != list:
            return self.list_type(result)
        else:
            return result


class EnumField(fields.Field):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super(EnumField, self).__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return value.name

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return self.enum[value]
        except ValueError as error:
            raise ValidationError(f"{value} is no correct value of enum {self.enum.__name__}.") from error


class CompatibilityField(fields.Field):
    _CHECK_ATTRIBUTE = False

    def __init__(self, field, serialize=None, deserialize=None, *args, **kwargs):
        self.field: fields.Field = field
        self._serialize_func = serialize
        self._deserialize_func = deserialize
        super().__init__(*args, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        serialize_func = self._serialize_func
        if isinstance(serialize_func, str):
            serialize_func = marshmallow.utils.callable_or_raise(
                getattr(self.parent, serialize_func, None)
            )
        if serialize_func:
            value = serialize_func(value, attr, obj, **kwargs)
        return self.field._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value, attr, obj, **kwargs):
        value = self.field._deserialize(value, attr, obj, **kwargs)
        deserialize_func = self._deserialize_func
        if isinstance(deserialize_func, str):
            deserialize_func = marshmallow.utils.callable_or_raise(
                getattr(self.parent, deserialize_func, None)
            )
        if deserialize_func:
            value = deserialize_func(value, attr, obj, **kwargs)
        return value


class VariantSchemaField(fields.Nested):
    VARIANT_KEY = "$variant"

    def __init__(self, default_schema, *alternatives: typing.Type[Schema], **kwargs):
        self.alternatives = {type(a().create_object()).__name__: a() for a in alternatives}
        super().__init__(default_schema, **kwargs)

    def _serialize(self, value: typing.Any, attr: typing.Optional[str], obj: typing.Any, **kwargs):
        schema = self.alternatives.get(type(value).__name__, None)
        if schema:
            result = schema.dump(value)
            result[self.VARIANT_KEY] = type(value).__name__
            return result
        else:
            return super()._serialize(value, attr, obj, **kwargs)

    def _deserialize(self, value: typing.Any, attr: typing.Optional[str],
                     data: typing.Optional[typing.Mapping[str, typing.Any]], **kwargs):
        if self.VARIANT_KEY in value:
            schema_name = value.pop(self.VARIANT_KEY)
            return self.alternatives[schema_name].load(value)
        else:
            return super()._deserialize(value, attr, data, **kwargs)


class NumpyField(fields.List):
    import numpy

    def __init__(self, **kwargs):
        super().__init__(fields.Field, **kwargs)

    def _deserialize(self, value, attr, obj, **kwargs):
        stack = [value]

        while stack:
            elem = stack.pop()
            for i, e in enumerate(elem):
                if type(e) == list:
                    stack.append(e)
                elif type(e) == str:
                    elem[i] = float(math.nan)
                elif math.isfinite(e):
                    continue
                else:
                    raise NotImplementedError()

        arr = self.numpy.array(value)
        return arr

    def _serialize(self, value, attr, obj, **kwargs):
        list_val = value.tolist()

        stack = [list_val]

        while stack:
            elem = stack.pop()
            for i, e in enumerate(elem):
                if type(e) == list:
                    stack.append(e)
                elif math.isfinite(e):
                    continue
                elif math.isnan(e):
                    elem[i] = 'nan'
                elif e == math.inf:
                    elem[i] = 'inf'
                elif e == -math.inf:
                    elem[i] = '-inf'
                else:
                    raise NotImplementedError

        return super()._serialize(list_val, attr, obj)

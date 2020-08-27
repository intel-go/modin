# Licensed to Modin Development Team under one or more contributor license agreements.
# See the NOTICE file distributed with this work for additional information regarding
# copyright ownership.  The Modin Development Team licenses this file to you under the
# Apache License, Version 2.0 (the "License"); you may not use this file except in
# compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

from modin.backends.pandas.query_compiler import PandasQueryCompiler, _dt_prop_map

import pandas
import numpy as np
import re

from pandas.core.dtypes.common import is_scalar


def DFAlgNotSupported(fn_name):
    def fn(*args, **kwargs):
        raise NotImplementedError(
            "{} is not yet suported in DFAlgQueryCompiler".format(fn_name)
        )

    return fn


def _property_wrapper_builder(fn_name):
    def property_wrapper(df):
        return getattr(df, fn_name)

    return property_wrapper


def _series_wrapper_builder(fn):
    def series_wrapper(df, *args, **kwargs):
        result = fn(df.squeeze(axis=1), *args, **kwargs)
        if is_scalar(result):
            result = pandas.Series(result)
        return result

    return series_wrapper


def _build_wrapper(fn, fn_name=None):
    def wrapper(self, *args, **kwargs):
        return self.default_to_pandas(fn, *args, **kwargs)

    if fn_name is None:
        fn_name = fn.__name__

    # setting proper function name that will be printed in default to pandas warning
    wrapper.__name__ = fn_name
    return wrapper


def _build_default_method(obj, fn_name):
    fn = getattr(obj, fn_name)
    assert callable(fn) or type(fn) == property

    if type(fn) == property:
        fn = _property_wrapper_builder(fn_name)

    if obj == pandas.Series:
        fn = _series_wrapper_builder(fn)

    return _build_wrapper(fn, fn_name)


def _build_dt_method(fn_name):
    fn_name = re.findall(r"dt_(.*)", fn_name)[0]
    fn = _dt_prop_map(fn_name)
    return _build_wrapper(fn, fn_name)


def _build_default_groupby(name):
    return DFAlgNotSupported(name)


def _pick_group(name):
    for group_name, picker in _group_pickers.items():
        if picker(name):
            return group_name
    return None


def add_defaults(cls):
    all_methods, implemented_methods = map(
        lambda x: frozenset(x.__dict__.keys()), [PandasQueryCompiler, cls]
    )
    not_implemented = all_methods.difference(implemented_methods)

    replacable = {key: [] for key in _group_pickers.keys()}

    for name in not_implemented:
        group_name = _pick_group(name)
        if group_name is not None:
            replacable[group_name].append(name)

    for group_name, methods in replacable.items():
        builder = _default_builders[group_name]
        for method in methods:
            setattr(cls, method, builder(method))

    not_supported = not_implemented.difference(
        np.concatenate(list(replacable.values()))
    )
    for name in not_supported:
        setattr(cls, name, DFAlgNotSupported(name))

    cls.__abstractmethods__ = frozenset(cls.__abstractmethods__).difference(
        cls.__dict__.keys()
    )

    return cls


_group_pickers = {
    "dataframe": lambda name: hasattr(pandas.DataFrame, name),
    "series": lambda name: hasattr(pandas.Series, name)
    and not hasattr(pandas.DataFrame, name),
    "groupby": lambda name: re.match(r"groupby_.*", name) is not None,
    "dt_methods": lambda name: re.match(r"dt_.*", name) is not None,
}

_default_builders = {
    "dataframe": lambda name: _build_default_method(pandas.DataFrame, name),
    "series": lambda name: _build_default_method(pandas.Series, name),
    "groupby": _build_default_groupby,
    "dt_methods": _build_dt_method,
}

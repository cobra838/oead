import pytest

import oead


class DefaultValue:
    pass


def test_parameter_map_mapping_operations():
    params = oead.aamp.ParameterMap()
    first = oead.aamp.Name("First")
    second = oead.aamp.Name("Second")
    third = oead.aamp.Name("Third")
    missing = oead.aamp.Name("Missing")
    first_value = oead.aamp.Parameter(1)
    second_value = oead.aamp.Parameter(2)
    third_value = oead.aamp.Parameter(3)

    params[first] = first_value
    assert len(params) == 1
    assert first in params
    assert missing not in params
    assert params[first] == first_value
    assert params.get(first) == first_value
    default = DefaultValue()
    assert params.get(missing, default) is default
    with pytest.raises(KeyError):
        params[missing]
    with pytest.raises(KeyError):
        params.get(missing)

    params[second] = second_value
    assert list(params.keys()) == [first, second]
    assert list(params.values()) == [first_value, second_value]
    assert list(params.items()) == [(first, first_value), (second, second_value)]

    keys = params.keys()
    values = params.values()
    items = params.items()
    params[third] = third_value
    assert list(keys) == [first, second, third]
    assert list(values) == [first_value, second_value, third_value]
    assert list(items) == [
        (first, first_value),
        (second, second_value),
        (third, third_value),
    ]

    del params[first]
    assert len(params) == 2
    assert first not in params
    with pytest.raises(KeyError):
        del params[first]

    params.clear()
    assert not params

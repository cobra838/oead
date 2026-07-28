import pytest
import oead

from utils import make_test_cases

cases_bin, data_bin = make_test_cases("byml/files/*.byml")
cases_text, data_text = make_test_cases("byml/files/*.yml")

# Check new Dictionary = old Hash
def test_byml_hash_alias():
    assert oead.byml.Hash is oead.byml.Dictionary


def test_byml_nested_containers_are_mutable():
    data = oead.byml.Dictionary(
        {
            "array": oead.byml.Array([oead.S32(1)]),
            "dictionary": oead.byml.Dictionary({"value": oead.S32(1)}),
        }
    )

    data["array"].append(oead.S32(2))
    data["dictionary"]["value"] = oead.S32(2)

    assert len(data["array"]) == 2
    assert data["dictionary"]["value"] == oead.S32(2)


def test_byml_roundtrip_mono_typed_array():
    # Little-endian BYML v10 containing a MonoTypedArray of two Int values: 42 and -5.
    data = bytes.fromhex(
        "59420a00000000000000000010000000"
        "c8020000d10000002a000000fbffffff"
    )

    array = oead.byml.from_binary(data)
    assert isinstance(array, oead.byml.Array)
    assert [int(value) for value in array] == [42, -5]
    assert oead.byml.to_binary(array, big_endian=False, version=10) == data


@pytest.mark.parametrize("file", cases_bin)
def test_byml_roundtrip_bin(file):
    data = oead.byml.from_binary(data_bin[file])
    serialized = oead.byml.to_binary(data, big_endian=False, version=2)
    data2 = oead.byml.from_binary(serialized)
    assert data == data2


@pytest.mark.parametrize("file", cases_bin)
def test_byml_roundtrip_bin_big_endian(file):
    data = oead.byml.from_binary(data_bin[file])
    serialized = oead.byml.to_binary(data, big_endian=True, version=2)
    data2 = oead.byml.from_binary(serialized)
    assert data == data2


@pytest.mark.parametrize("file", cases_text)
def test_byml_roundtrip_text(file):
    data = oead.byml.from_text(data_text[file])
    serialized = oead.byml.to_text(data)
    data2 = oead.byml.from_text(serialized)
    assert data == data2


@pytest.mark.parametrize("file", cases_bin)
def test_byml_roundtrip_bin_to_text(file):
    data = oead.byml.from_binary(data_bin[file])
    serialized = oead.byml.to_text(data)
    data2 = oead.byml.from_text(serialized)
    assert data == data2


@pytest.mark.parametrize("file", cases_text)
def test_byml_roundtrip_text_to_bin(file):
    data = oead.byml.from_text(data_text[file])
    serialized = oead.byml.to_binary(data, big_endian=False, version=2)
    data2 = oead.byml.from_binary(serialized)
    assert data == data2

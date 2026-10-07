import pytest
import oead
import struct

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


def test_byml_v2_does_not_align_between_binary_values():
    array = oead.byml.Array([oead.Bytes([0x41]), oead.Bytes([0x42, 0x43])])
    data = bytes(oead.byml.to_binary(array, big_endian=False, version=2))
    root_offset = struct.unpack_from("<I", data, 12)[0]
    first, second = struct.unpack_from("<II", data, root_offset + 8)

    assert data[:4] == b"YB\x02\x00"
    assert first % 4 == 0
    assert second == first + 4 + 1
    assert list(oead.byml.from_binary(data)) == list(array)


def test_byml_equal_maps_reuse_binary_node():
    first = oead.byml.Dictionary()
    second = oead.byml.Dictionary()
    for index in range(16):
        first[f"key_{index}"] = oead.S32(index)
    for index in reversed(range(16)):
        second[f"key_{index}"] = oead.S32(index)

    data = bytes(oead.byml.to_binary(oead.byml.Array([first, second]), False, 2))
    root_offset = struct.unpack_from("<I", data, 12)[0]
    first_offset, second_offset = struct.unpack_from("<II", data, root_offset + 8)

    assert first == second
    assert first_offset == second_offset


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

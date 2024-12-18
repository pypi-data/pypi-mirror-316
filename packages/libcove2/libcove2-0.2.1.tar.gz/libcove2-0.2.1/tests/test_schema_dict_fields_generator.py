import json

import pytest

from libcove2.common import schema_dict_fields_generator


@pytest.fixture
def schema_0_3():
    """Schema for BODS 0.3"""
    with open("tests/fixtures/schema-0-3-0.json", "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def schema_0_4():
    """Schema for BODS 0.4"""
    with open("tests/fixtures/schema-0-4-0.json", "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def rdls_schema_0_2():
    """Schema for RDLS 0.2"""
    with open("tests/fixtures/rdls-schema-0-2-0.json", "r") as read_file:
        return json.load(read_file)


@pytest.fixture
def ofds_schema_0_3():
    """Schema for OFDS 0.3"""
    with open("tests/fixtures/ofds-schema-0-3-0.json", "r") as read_file:
        return json.load(read_file)


def test_schema_dict_fields_generator_0_3(schema_0_3):

    schema_fields = set(schema_dict_fields_generator(schema_0_3))

    assert len(schema_fields) == 138


def test_schema_dict_fields_generator_0_4(schema_0_4):

    schema_fields = set(schema_dict_fields_generator(schema_0_4))

    assert len(schema_fields) == 139


def test_schema_dict_fields_generator_rdls_0_2(rdls_schema_0_2):

    schema_fields = set(schema_dict_fields_generator(rdls_schema_0_2))

    assert len(schema_fields) == 228


def test_schema_dict_fields_generator_ofds_0_3(ofds_schema_0_3):

    schema_fields = set(schema_dict_fields_generator(ofds_schema_0_3))

    assert len(schema_fields) == 133

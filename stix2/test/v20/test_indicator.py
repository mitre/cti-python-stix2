import datetime as dt
import re

import pytest
import pytz

import stix2

from .constants import FAKE_TIME, INDICATOR_ID, INDICATOR_KWARGS

EXPECTED_INDICATOR = """{
    "type": "indicator",
    "id": "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
    "created": "2017-01-01T00:00:01.000Z",
    "modified": "2017-01-01T00:00:01.000Z",
    "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    "valid_from": "1970-01-01T00:00:01Z",
    "labels": [
        "malicious-activity"
    ]
}"""

EXPECTED_INDICATOR_REPR = "Indicator(" + " ".join("""
    type='indicator',
    id='indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7',
    created='2017-01-01T00:00:01.000Z',
    modified='2017-01-01T00:00:01.000Z',
    pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
    valid_from='1970-01-01T00:00:01Z',
    labels=['malicious-activity']
""".split()) + ")"


def test_indicator_with_all_required_properties():
    now = dt.datetime(2017, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    epoch = dt.datetime(1970, 1, 1, 0, 0, 1, tzinfo=pytz.utc)

    ind = stix2.v20.Indicator(
        type="indicator",
        id=INDICATOR_ID,
        created=now,
        modified=now,
        pattern="[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
        valid_from=epoch,
        labels=['malicious-activity'],
    )

    assert ind.revoked is False
    assert str(ind) == EXPECTED_INDICATOR
    rep = re.sub(r"(\[|=| )u('|\"|\\\'|\\\")", r"\g<1>\g<2>", repr(ind))
    assert rep == EXPECTED_INDICATOR_REPR


def test_indicator_autogenerated_properties(indicator):
    assert indicator.type == 'indicator'
    assert indicator.id == 'indicator--00000000-0000-4000-8000-000000000001'
    assert indicator.created == FAKE_TIME
    assert indicator.modified == FAKE_TIME
    assert indicator.labels == ['malicious-activity']
    assert indicator.pattern == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator.valid_from == FAKE_TIME

    assert indicator['type'] == 'indicator'
    assert indicator['id'] == 'indicator--00000000-0000-4000-8000-000000000001'
    assert indicator['created'] == FAKE_TIME
    assert indicator['modified'] == FAKE_TIME
    assert indicator['labels'] == ['malicious-activity']
    assert indicator['pattern'] == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"
    assert indicator['valid_from'] == FAKE_TIME


def test_indicator_type_must_be_indicator():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(type='xxx', **INDICATOR_KWARGS)

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == "type"
    assert excinfo.value.reason == "must equal 'indicator'."
    assert str(excinfo.value) == "Invalid value for Indicator 'type': must equal 'indicator'."


def test_indicator_id_must_start_with_indicator():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(id='my-prefix--', **INDICATOR_KWARGS)

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == "id"
    assert excinfo.value.reason == "must start with 'indicator--'."
    assert str(excinfo.value) == "Invalid value for Indicator 'id': must start with 'indicator--'."


def test_indicator_required_properties():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.v20.Indicator()

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.properties == ["labels", "pattern"]
    assert str(excinfo.value) == "No values for required properties for Indicator: (labels, pattern)."


def test_indicator_required_property_pattern():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.v20.Indicator(labels=['malicious-activity'])

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.properties == ["pattern"]


def test_indicator_created_ref_invalid_format():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(created_by_ref='myprefix--12345678', **INDICATOR_KWARGS)

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == "created_by_ref"


def test_indicator_revoked_invalid():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(revoked='no', **INDICATOR_KWARGS)

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == "revoked"
    assert excinfo.value.reason == "must be a boolean value."


def test_cannot_assign_to_indicator_attributes(indicator):
    with pytest.raises(stix2.exceptions.ImmutableError) as excinfo:
        indicator.valid_from = dt.datetime.now()

    assert str(excinfo.value) == "Cannot modify 'valid_from' property in 'Indicator' after creation."


def test_invalid_kwarg_to_indicator():
    with pytest.raises(stix2.exceptions.ExtraPropertiesError) as excinfo:
        stix2.v20.Indicator(my_custom_property="foo", **INDICATOR_KWARGS)

    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.properties == ['my_custom_property']
    assert str(excinfo.value) == "Unexpected properties for Indicator: (my_custom_property)."


def test_created_modified_time_are_identical_by_default():
    """By default, the created and modified times should be the same."""
    ind = stix2.v20.Indicator(**INDICATOR_KWARGS)

    assert ind.created == ind.modified


@pytest.mark.parametrize(
    "data", [
        EXPECTED_INDICATOR,
        {
            "type": "indicator",
            "id": "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
            "created": "2017-01-01T00:00:01Z",
            "modified": "2017-01-01T00:00:01Z",
            "labels": [
                "malicious-activity",
            ],
            "pattern": "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']",
            "valid_from": "1970-01-01T00:00:01Z",
        },
    ],
)
def test_parse_indicator(data):
    idctr = stix2.parse(data, version="2.0")

    assert idctr.type == 'indicator'
    assert idctr.id == INDICATOR_ID
    assert idctr.created == dt.datetime(2017, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    assert idctr.modified == dt.datetime(2017, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    assert idctr.valid_from == dt.datetime(1970, 1, 1, 0, 0, 1, tzinfo=pytz.utc)
    assert idctr.labels[0] == "malicious-activity"
    assert idctr.pattern == "[file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e']"


def test_invalid_indicator_pattern():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(
            labels=['malicious-activity'],
            pattern="file:hashes.MD5 = 'd41d8cd98f00b204e9800998ecf8427e'",
        )
    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == 'pattern'
    assert 'input is missing square brackets' in excinfo.value.reason

    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v20.Indicator(
            labels=['malicious-activity'],
            pattern='[file:hashes.MD5 = "d41d8cd98f00b204e9800998ecf8427e"]',
        )
    assert excinfo.value.cls == stix2.v20.Indicator
    assert excinfo.value.prop_name == 'pattern'
    assert 'mismatched input' in excinfo.value.reason

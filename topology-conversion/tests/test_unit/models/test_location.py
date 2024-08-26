import pytest
from models import Location

# Sample valid data
valid_location_data = {
    "address": "123 Example St",
    "latitude": 40.7128,
    "longitude": -74.0060
}

# Sample invalid data
invalid_addresses = [
    None,
]

invalid_latitudes = [
    None,
    91.0,
    -91.0,
]

invalid_longitudes = [
    None,
    91.0,
    -91.0,
]

def test_location_initialization():
    """Test valid initialization"""
    location = Location(
        address="123 Example St",
        latitude=40.7128,
        longitude=-74.0060
    )
    assert location.address == "123 Example St"
    assert location.latitude == 40.7128
    assert location.longitude == -74.0060

@pytest.mark.parametrize("address", invalid_addresses)
def test_invalid_address(address):
    """Test invalid address"""
    location = Location()
    with pytest.raises(ValueError):
        location.address = address
        location.latitude=40.7128
        location.longitude=-74.0060

@pytest.mark.parametrize("latitude", invalid_latitudes)
def test_invalid_latitude(latitude):
    """Test invalid latitude"""
    location = Location()
    with pytest.raises(ValueError):
        location.address="123 Example St"
        location.latitude=latitude
        location.longitude=-74.0060

@pytest.mark.parametrize("longitude", invalid_longitudes)
def test_invalid_longitude(longitude):
    """Test invalid longitude"""
    location = Location()
    with pytest.raises(ValueError):
        location.address="123 Example St"
        location.latitude=40.7128
        location.longitude=longitude

def test_from_dict():
    """Test from_dict method with valid data"""
    location = Location.from_dict(valid_location_data)
    assert location.address == "123 Example St"
    assert location.latitude == 40.7128
    assert location.longitude == -74.0060

def test_from_dict_invalid_data():
    """Test from_dict method with invalid data"""
    invalid_data = {"address": None, "latitude": 40.7128, "longitude": -74.0060}
    with pytest.raises(ValueError):
        Location.from_dict(invalid_data)

    invalid_data = {"address": "123 Example St", "latitude": None, "longitude": -74.0060}
    with pytest.raises(ValueError):
        Location.from_dict(invalid_data)

    invalid_data = {"address": "123 Example St", "latitude": 40.7128, "longitude": None}
    with pytest.raises(ValueError):
        Location.from_dict(invalid_data)

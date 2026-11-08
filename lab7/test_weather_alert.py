import math

from hypothesis import given, strategies as st
from weather_alert import parse_reading, wind_category, rainfall_spread

WIND_CATEGORIES = {'warning', 'advisory', 'none'}


# ---------- parse_reading ----------

# Fuzz with arbitrary text or None: must never raise; any accepted reading must be sane
@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    result = parse_reading(s)
    if result is not None:
        temp, humidity = result
        assert math.isfinite(temp)
        assert 0 <= humidity <= 100

# Well-formed "temp/humidity" strings must round-trip to the original values
@given(st.floats(allow_nan=False, allow_infinity=False), st.integers(min_value=0, max_value=100))
def test_parse_reading_valid(temp, humidity):
    assert parse_reading(f"{temp}/{humidity}") == (temp, humidity)

# Humidity is a percentage, so values outside 0-100 must be rejected
@given(st.floats(allow_nan=False, allow_infinity=False),
       st.integers(max_value=-1) | st.integers(min_value=101))
def test_parse_reading_bad_humidity(temp, humidity):
    assert parse_reading(f"{temp}/{humidity}") is None


# ---------- wind_category ----------

# Fuzz with arbitrary text or None: must never raise and only return a known category or None
@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    assert wind_category(s) in WIND_CATEGORIES | {None}

# Valid speeds (whole or decimal) must be graded using the 39 / 89 km/h thresholds
@given(st.integers(min_value=0, max_value=500) | st.floats(min_value=0, max_value=500))
def test_wind_category_thresholds(speed):
    if speed >= 89:
        expected = 'warning'
    elif speed >= 39:
        expected = 'advisory'
    else:
        expected = 'none'
    assert wind_category(str(speed)) == expected

# A negative wind speed is physically impossible and must be rejected
@given(st.integers(max_value=-1) | st.floats(max_value=-0.001, allow_infinity=False))
def test_wind_category_negative(speed):
    assert wind_category(str(speed)) is None


# ---------- rainfall_spread ----------

# Fuzz with arbitrary text or None: must never raise; any result must be finite and non-negative
@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    result = rainfall_spread(s)
    if result is not None:
        assert math.isfinite(result)
        assert result >= 0

# Valid CSV of non-negative readings must give exactly max - min
@given(st.lists(st.floats(min_value=0, max_value=1e6), min_size=1))
def test_rainfall_spread_valid(readings):
    csv = ','.join(str(r) for r in readings)
    assert rainfall_spread(csv) == max(readings) - min(readings)

# Rainfall cannot be negative, so any negative reading must be rejected
@given(st.lists(st.floats(min_value=0, max_value=1e6)),
       st.floats(max_value=-0.001, allow_infinity=False))
def test_rainfall_spread_negative(readings, negative):
    csv = ','.join(str(r) for r in readings + [negative])
    assert rainfall_spread(csv) is None

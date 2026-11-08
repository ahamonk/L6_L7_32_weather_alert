import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Code (line) coverage: each test executes at least one return/raise line
# that no other test reaches, so together they run every statement.

# wind_alert
def test_wind_warning():
    assert wind_alert(100) == "warning"

def test_wind_watch():
    assert wind_alert(70) == "watch"

def test_wind_advisory():
    assert wind_alert(50) == "advisory"

def test_wind_none():
    assert wind_alert(10) == "none"

# rain_alert
def test_heavy_rain_saturated_soil():
    assert rain_alert(60, True) == "warning"

def test_heavy_rain_dry_soil():
    assert rain_alert(60, False) == "watch"

def test_moderate_rain_saturated_soil():
    assert rain_alert(20, True) == "watch"

def test_moderate_rain_dry_soil():
    assert rain_alert(20, False) == "advisory"

def test_light_rain():
    assert rain_alert(5, False) == "none"

# heat_alert
def test_heat_warning():
    assert heat_alert(46, 30) == "warning"

def test_heat_watch():
    assert heat_alert(41, 30) == "watch"

def test_heat_advisory():
    assert heat_alert(36, 30) == "advisory"

def test_heat_none():
    assert heat_alert(20, 30) == "none"

def test_heat_humidity_raises_index():
    # 38 + (80 - 40) * 0.1 = 42 -> watch; runs the humidity adjustment line
    assert heat_alert(38, 80) == "watch"

# overall_alert
def test_overall_picks_worst():
    assert overall_alert(["advisory", "warning", "watch"]) == "warning"

def test_overall_unknown_alert():
    with pytest.raises(ValueError):
        overall_alert(["tornado"])

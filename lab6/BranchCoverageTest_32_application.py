import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Branch coverage: every decision is driven both True and False.
# Threshold decisions are tested exactly at the boundary (True) and
# just below it (False).

# wind_alert: speed_kmh >= 89
def test_wind_at_89_is_warning():
    assert wind_alert(89) == "warning"

def test_wind_at_88_not_warning():
    assert wind_alert(88) == "watch"

# wind_alert: speed_kmh >= 62
def test_wind_at_62_is_watch():
    assert wind_alert(62) == "watch"

def test_wind_at_61_not_watch():
    assert wind_alert(61) == "advisory"

# wind_alert: speed_kmh >= 39
def test_wind_at_39_is_advisory():
    assert wind_alert(39) == "advisory"

def test_wind_at_38_is_none():
    assert wind_alert(38) == "none"

# rain_alert: mm_per_hour >= 50 True, then soil_saturated True/False
def test_rain_at_50_saturated():
    assert rain_alert(50, True) == "warning"

def test_rain_at_50_not_saturated():
    assert rain_alert(50, False) == "watch"

# rain_alert: mm_per_hour >= 50 False, >= 10 True, then soil_saturated True/False
def test_rain_at_49_saturated():
    assert rain_alert(49, True) == "watch"

def test_rain_at_10_not_saturated():
    assert rain_alert(10, False) == "advisory"

# rain_alert: mm_per_hour >= 10 False
def test_rain_at_9_is_none():
    assert rain_alert(9, True) == "none"

# heat_alert: humidity > 40 False (index stays at temp_c)
def test_heat_humidity_40_not_adjusted():
    assert heat_alert(34, 40) == "none"

# heat_alert: humidity > 40 True (index raised above temp_c)
def test_heat_humidity_60_adjusted():
    # 34 + (60 - 40) * 0.1 = 36 -> advisory
    assert heat_alert(34, 60) == "advisory"

# heat_alert: index >= 45
def test_heat_index_45_is_warning():
    assert heat_alert(45, 20) == "warning"

def test_heat_index_44_not_warning():
    assert heat_alert(44, 20) == "watch"

# heat_alert: index >= 40
def test_heat_index_40_is_watch():
    assert heat_alert(40, 20) == "watch"

def test_heat_index_39_not_watch():
    assert heat_alert(39, 20) == "advisory"

# heat_alert: index >= 35
def test_heat_index_35_is_advisory():
    assert heat_alert(35, 20) == "advisory"

# overall_alert: loop body never runs
def test_overall_empty_list():
    assert overall_alert([]) == "none"

# overall_alert: SEVERITY[alert] > SEVERITY[worst] False ("none" is not worse than "none")
def test_overall_only_none():
    assert overall_alert(["none"]) == "none"

# overall_alert: comparison True first, then False for a less severe alert
def test_overall_later_alert_less_severe():
    assert overall_alert(["warning", "advisory"]) == "warning"

# overall_alert: alert not in SEVERITY False for "watch", then True for "bogus"
def test_overall_unknown_after_valid_alert():
    with pytest.raises(ValueError):
        overall_alert(["watch", "bogus"])

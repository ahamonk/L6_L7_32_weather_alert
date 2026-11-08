import math

def parse_reading(text):
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    try:
        temp, humidity = float(parts[0]), int(parts[1])
    except ValueError:
        return None
    if not math.isfinite(temp) or not 0 <= humidity <= 100:
        return None
    return temp, humidity

def wind_category(speed_text):
    if not isinstance(speed_text, str):
        return None
    try:
        speed = float(speed_text)
    except ValueError:
        return None
    if not math.isfinite(speed) or speed < 0:
        return None
    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'

def rainfall_spread(readings_csv):
    if not isinstance(readings_csv, str):
        return None
    try:
        readings = [float(r) for r in readings_csv.split(',')]
    except ValueError:
        return None
    if any(not math.isfinite(r) or r < 0 for r in readings):
        return None
    return max(readings) - min(readings)

def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result if result is not None else "Invalid input")

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result if result is not None else "Invalid input")

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()

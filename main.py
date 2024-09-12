import sys
from datetime import datetime, timedelta, timezone
import calendar

def convert_to_unix_timestamp(date_str):
    # Define the date format
    date_format = "%d-%m-%Y"

    # Parse the date string into a datetime object
    try:
        local_date_obj = datetime.strptime(date_str, date_format)
    except ValueError:
        raise ValueError("Invalid date format. Use 'dd-mm-yyyy'.")

    # Define the PST time zone offset
    pst_offset = timedelta(hours=-8)  # PST is UTC-8

    # Convert local time to UTC
    utc_date_obj = local_date_obj - pst_offset

    # Convert the UTC datetime object to a Unix timestamp (in seconds)
    unix_timestamp_seconds = calendar.timegm(utc_date_obj.utctimetuple())

    # Convert to milliseconds
    unix_timestamp_millis = unix_timestamp_seconds * 1000

    return unix_timestamp_millis

def convert_to_pst(unix_timestamp):
    # Check if the Unix timestamp is within the valid range (in milliseconds)
    if unix_timestamp < -62135596800000 or unix_timestamp > 253402300799000:
        raise ValueError("Unix timestamp out of range for datetime module")

    # Convert the Unix timestamp to seconds for conversion
    unix_timestamp_seconds = unix_timestamp // 1000

    # Convert the Unix timestamp (in seconds) to a datetime object in UTC
    utc_date_obj = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=unix_timestamp_seconds)

    # Define the PST time zone offset
    pst_offset = timedelta(hours=-8)  # PST is UTC-8

    # Convert UTC to PST
    pst_date_obj = utc_date_obj + pst_offset

    # Format the datetime object as a string
    date_str = pst_date_obj.strftime("%d-%m-%Y %H:%M:%S PST")

    return date_str

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <date_str_or_timestamp>")
        sys.exit(1)

    input_value = sys.argv[1]

    try:
        # Check if the input is a number (Unix timestamp in milliseconds)
        unix_timestamp = int(input_value)
        print(convert_to_pst(unix_timestamp))
    except ValueError:
        # If not a number, treat it as a date string
        unix_timestamp = convert_to_unix_timestamp(input_value)
        print(unix_timestamp)

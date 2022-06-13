import datetime as dt

TIMESTAMP_FORMAT = "%H:%M:%S"

def get_formatted_time():
  """
  Returns the currrent UTC hour, minute, and second formatted according to `TIMESTAMP_FORMAT`
  """
  return dt.datetime.now().strftime(TIMESTAMP_FORMAT)
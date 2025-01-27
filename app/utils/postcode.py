import re

def is_valid_us_postcode(postcode):
  """
  This function uses a regular expression to check if a string resembles a valid US postcode format (XXXXX or XXXXX-XXXX).
  """
  regex = r"\d{5}(?:[-\s]\d{4})?$"
  return bool(re.match(regex, postcode))
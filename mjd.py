#! /usr/bin/env python
#

import sys
import datetime
from astropy.time import Time

def mjd_to_datetime(mjd):
    """Converts MJD to a datetime object (UTC)."""
    jd = mjd + 2400000.5  # Convert MJD to Julian Date (JD)
    t = Time(jd, format='jd') # Create an astropy Time object
    return t.to_datetime() # Convert to datetime object

# Example usage:
# mjd_value = 58134.09699299725
# datetime_object = mjd_to_datetime(mjd_value)
# print(datetime_object) # Output will be a datetime object

for mjd in sys.argv[1:]:
   print(mjd_to_datetime(float(mjd)))


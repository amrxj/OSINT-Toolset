import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

#decimal format conversion

def conversion_decimal(dms, reference):
    degrees, minutes, seconds = dms
    decimal = degrees[0] / degrees[1] + \
              minutes[0] / (minutes[1] * 60.0) + \
              seconds[0] / (seconds[1] * 3600.0)
    if reference in ['S', 'W']:
        decimal = -decimal
    return decimal

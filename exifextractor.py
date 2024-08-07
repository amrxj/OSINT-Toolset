import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from tkinter import *
from tkinter import Tk, Button, filedialog

#decimal format conversion


#Explanation of decimal conversion: 
#converts degrees minutes seconds into decimal degree
#dms is a tuple containing all three, each are expected to be
#an IFDRational object from exif data. 
#reference indicates direction (it's a string)
#EXTRA: An IFDRational object in the context of image metadata represents a rational number, specifically used to store precise values such as GPS coordinates. It consists of a numerator and a denominator, allowing for accurate representation of fractional values in the image's EXIF data.
def conversion_decimal(dms, reference):
    degrees = dms[0].numerator / dms[0].denominator
    minutes = dms[1].numerator / dms[1].denominator
    seconds = dms[2].numerator / dms[2].denominator

    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if reference in ['S', 'W']:
        decimal = -decimal
    return decimal

def openFile():
    filepath = filedialog.askopenfilename()
    if filepath:
        process_image(filepath)
    
    root.quit() #closes correctly
 

# Gathering EXIF information from images.
filename = openFile()

def process_image(filename):
    with Image.open(filename) as img:

        exif_data = img._getexif()
        gps_data = {}

        #if it has exif data
        if exif_data:
            #get gps data
        
            for tag_id in exif_data:
                #get tags name
                tag = TAGS.get(tag_id, tag_id)
                if tag == 'GPSInfo':
                    for key, val in exif_data[tag_id].items():
                        decoded = GPSTAGS.get(key, key)
                        gps_data[decoded] = val

        #check if contains latitude and longitude
        if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
            lat = conversion_decimal(gps_data['GPSLatitude'], gps_data['GPSLatitudeRef'])
            long = conversion_decimal(gps_data['GPSLongitude'], gps_data['GPSLongitudeRef'])
            print(f"Latitude: {lat}, Longitude: {long}")
        else:
                print("No GPS data available.")

if __name__ == "__main__":
    root = Tk()
    Button(root, text="Open Image", command=lambda: openFile(root)).pack()
    root.mainloop()
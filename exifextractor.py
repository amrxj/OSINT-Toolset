import os
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import tkinter as tk
from tkinter import filedialog
import whois
import validators




def domain_lookup(dom):
    if validators.domain(dom):

        try:
            dom_info = whois.whois(dom)
            return dom_info
        
        except:
            return f"{dom} isn't registered or legit"
        
    else:
            return f"Enter a proper domain"



def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title = "Select a File")
    return file_path

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select a folder")
    return folder_path

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



# Gathering EXIF information from images.
def exifgathering(filename):
    try:
        with Image.open(filename) as img:

            exif_data = img._getexif()
            gps_data = {}

            #if it has exif data
            if exif_data:
                print("\nEXIF data located!")
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
                print(f"Google Maps: https://maps.google.com/?q={lat},{long}")
            else:
                print("No GPS data available.")
            
    except Exception as e:
                    print(f"error has occured: {e}")

def multi_search(directory):
    supported_ext = ('.jpg', '.tiff')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_ext):
                exifgathering(os.path.join(root, file))

def info_data(filepath):
            
        with Image.open(filepath) as img:
            exif_data = img._getexif()
            if exif_data:
                print("EXIF Data Located!")
                exif = {TAGS.get(k, k): v for k, v in exif_data.items()}
                
                camera_make = exif.get('Make', 'N/A')
                camera_model = exif.get('Model', 'N/A')
                software = exif.get('Software', 'N/A')
                date_time = exif.get('DateTime', 'N/A')

                print(f"Make: {camera_make}")
                print(f"Model: {camera_model}")
                print(f"OS: {software}")
                print(f"Date & Time: {date_time}")
                print(f"\n")
                
def banner(): 
    font = """


▄███▄      ▄  ▄█ ▄████      ▄███▄      ▄     ▄▄▄▄▀ █▄▄▄▄ ██   ▄█▄      ▄▄▄▄▀ ████▄ █▄▄▄▄ 
█▀   ▀ ▀▄   █ ██ █▀   ▀     █▀   ▀ ▀▄   █ ▀▀▀ █    █  ▄▀ █ █  █▀ ▀▄ ▀▀▀ █    █   █ █  ▄▀ 
██▄▄     █ ▀  ██ █▀▀        ██▄▄     █ ▀      █    █▀▀▌  █▄▄█ █   ▀     █    █   █ █▀▀▌  
█▄   ▄▀ ▄ █   ▐█ █          █▄   ▄▀ ▄ █      █     █  █  █  █ █▄  ▄▀   █     ▀████ █  █  
▀███▀  █   ▀▄  ▐  █         ▀███▀  █   ▀▄   ▀        █      █ ▀███▀   ▀              █   
        ▀          ▀                ▀               ▀      █                        ▀    
                                                          ▀                              
                                                          
                                                          
                                                           """ 
    print(font)

if __name__ == "__main__":
    banner()            


if __name__ == "__main__":
    mode = input(f"Enter 'single' to process a single image, 'multi' to process all images in a directory, and whois for domain lookup: ").lower()
    if mode == 'single':
       filename = select_file()
       if filename:
        exifgathering(filename)
        info_data(filename)
 
        
    elif mode == 'multi':
        directory = select_folder()
        if directory:
            multi_search(directory)
            info_data(directory)

    elif mode == 'whois':
        domain_input = input("Enter a domain you wish to verify: ")
        result = domain_lookup(domain_input)
        print(result)
    
    elif mode == 
    
    else:
        print("Invalid input. Please start the program again and choose a valid option.")
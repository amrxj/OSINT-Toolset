def info_data(filepath):
            
        with Image.open(filename) as img:
            exif_data = img._getexif()
            if exif_data:
                print("EXIF Data Located!")
                exif = {TAGS.get(k, k): v for k, v in exif_data.items()}
                print(exif)
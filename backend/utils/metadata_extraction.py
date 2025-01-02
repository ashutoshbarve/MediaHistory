from PIL import Image, ExifTags

def extract_metadata(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        metadata = {}
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                metadata[tag_name] = value
        else:
            metadata["message"] = "No EXIF data found"

        # Add basic image details
        metadata["image_size"] = image.size
        metadata["image_format"] = image.format
        return metadata
    except Exception as e:
        return {"error": str(e)}

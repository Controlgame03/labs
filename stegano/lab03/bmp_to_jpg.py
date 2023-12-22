from PIL import Image
from utils import ENCODED_IMAGE, JPEG_OUTPUT_FILE, CONVERTED_BMP_FROM_JPEG_FILE

def convert_bmp_to_jpeg(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.convert('RGB').save(output_path, 'JPEG',  quality=95, subsampling=0)
            print(f"Conversion successful. JPEG file saved at {output_path}")
    except Exception as e:
        print(f"Error: {e}")

def convert_jpeg_to_bmp(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, 'BMP',quality=95)
            print(f"Conversion successful. BMP file saved at {output_path}")
    except Exception as e:
        print(f"Error: {e}")

convert_bmp_to_jpeg(ENCODED_IMAGE, JPEG_OUTPUT_FILE)
convert_jpeg_to_bmp(JPEG_OUTPUT_FILE, ENCODED_IMAGE)
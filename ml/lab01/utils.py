import numpy as np
from PIL import Image

def readDatasetFile(filename):
   
    with open(filename, 'r') as file:
        lines = file.readlines()

    dataset_temp = []
    imageNameToIds = {}

    for i, line in enumerate(lines):
        values = line.strip().split(',')

        dataset_temp.append([int(0 if val == '0' else 1) for val in values[:-1]])
        if len(dataset_temp[-1]) != 1024:
            print(i)
        lastValue = values[-1].split('_')[0]
        
        if lastValue in imageNameToIds:
            imageNameToIds[lastValue].append(i)
        else:
            imageNameToIds[lastValue] = [i]

    dataset = np.array(dataset_temp)
    print(len(dataset))
    return dataset, imageNameToIds

def getBmpValues(filename):
    with open(filename, 'rb') as f:
        header = f.read(54)
        pixel_offset = int.from_bytes(header[10:14], byteorder='little')
        width = int.from_bytes(header[18:22], byteorder='little')
        height = int.from_bytes(header[22:26], byteorder='little')

        f.seek(0)
        fullImage = bytearray(f.read())

        return bytearray(fullImage), width, height, pixel_offset
    

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
        return x * (1 - x)

def readWeightFile(filename):
   
    with open(filename, 'r') as file:
        lines = file.read()
        return np.array(lines.split(',')[:-1],dtype=float)
    
def convert_bmp_to_jpeg(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.convert('RGB').save(output_path, 'JPEG',  quality=95, subsampling=0)
    except Exception as e:
        print(f"Error: {e}")

def convert_jpeg_to_bmp(input_path, output_path):
    try:
        with Image.open(input_path) as img:
            img.save(output_path, 'BMP',quality=95)
    except Exception as e:
        print(f"Error: {e}")
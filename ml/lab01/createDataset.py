from constatns import *
import random
from utils import *
import os

imageNameToCsv = {}

for dataset_folder in os.listdir(DATASET_IMAGE_PATH):
    if dataset_folder.find('.csv') != -1:
        continue
    
    for filename in os.listdir(DATASET_IMAGE_PATH + dataset_folder):
        fullImage, width, height, pixel_offset = getBmpValues(DATASET_IMAGE_PATH + dataset_folder + '/' + filename)
        dataset = []
        for i in range(pixel_offset, len(fullImage), 3):
            val = 0 if fullImage[i] > 220 else 1
            dataset.append(str(val))
        
        imageNameToCsv[filename] = dataset

imageNames = sorted(imageNameToCsv.keys(), key=lambda x: random.random())

i = 0
imageSize = 32*32 # Размер изображения, указывается в варианте

with open(DATASET_IMAGE_PATH + 'dataset.csv', 'w') as file:
    for imageName in imageNames:

        if len(imageNameToCsv[imageName]) == imageSize:

            i+=1 
            file.write(','.join(imageNameToCsv[imageName]) + ',' + imageName + '\n')

print(len(imageNameToCsv))
from PIL import Image
import os
import utils

originDatasetFolder = 'dataset_signes/' # директория с начальными картинками
resultDatasetFolder = 'dataset/' # директория с полным датасетом
dataset_transit_jpeg = 'transit_dataset_jpeg/'
dataset_transit_bmp = 'transit_dataset_bmp/'

if not os.path.exists(resultDatasetFolder):
    os.mkdir(resultDatasetFolder)

if not os.path.exists(dataset_transit_bmp):
    os.mkdir(dataset_transit_bmp)


if not os.path.exists(dataset_transit_jpeg):
    os.mkdir(dataset_transit_jpeg)

for folder in os.listdir(originDatasetFolder):
    fileIndex = 0
    resultImageFolder = resultDatasetFolder + folder + '/'

    for filename in os.listdir(originDatasetFolder + folder):
        
        transit_folder_jpeg = dataset_transit_jpeg + folder + '/'
        transit_folder_bmp = dataset_transit_bmp + folder + '/'
        
        if not os.path.exists(transit_folder_jpeg):
            os.mkdir(transit_folder_jpeg) 

        if not os.path.exists(transit_folder_bmp):
            os.mkdir(transit_folder_bmp) 

        utils.convert_bmp_to_jpeg(originDatasetFolder + folder + '/' + filename, transit_folder_jpeg + filename)
        utils.convert_jpeg_to_bmp(transit_folder_jpeg + filename, transit_folder_bmp + filename)
        
        im = Image.open(transit_folder_bmp + filename)

        if not os.path.exists(resultImageFolder):
            os.mkdir(resultImageFolder) 
        
        for i in range(-16, 21, 4):
            imageName = resultImageFolder + folder + '_' + str(fileIndex) + '.bmp'
            im_rotate = im.rotate(i, expand=True, fillcolor = 'white')
            img_resized = im_rotate.resize((32, 32))
            img_resized.save(imageName, 'BMP', quality=100)
            
            fileIndex += 1
                
        im.close()
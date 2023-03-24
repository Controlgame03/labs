import math
def saveInFileAndGetComponents(image, filename, position, startPos, width, height):
    step = 0
    storeImage = []
    for i in range(startPos, len(image)):
        if step != position:
            image[i] = 0
        else:
            storeImage.append(image[i])
        step = (step + 1) % 3
    imageFile = open(filename, 'wb')
    imageFile.write(bytes(image)) 
    imageFile.close()

    return storeImage

with open('kodim15.bmp', 'rb') as f:
    header = f.read(54)
    pixel_offset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')

    f.seek(0)
    fullImage = bytearray(f.read()) 

    imageR = saveInFileAndGetComponents(fullImage.copy(), 'red.bmp', 2, pixel_offset, width, height)
    imageG = saveInFileAndGetComponents(fullImage.copy(), 'green.bmp', 1, pixel_offset, width, height)
    imageB = saveInFileAndGetComponents(fullImage.copy(), 'blue.bmp', 0, pixel_offset, width, height)

def getR(image1, image2):
    mean1 = sum(image1) / (width * height)
    mean2 = sum(image2) / (width * height)
    cov = sum([(image1[i] - mean1) * (image2[i] - mean2) for i in range(len(image1))]) / (width * height)
    std1 = math.sqrt(sum([(image1[i] - mean1) ** 2 for i in range(len(image1))]) / (width * height - 1))
    std2 = math.sqrt(sum([(image2[i] - mean2) ** 2 for i in range(len(image2))]) / (width * height - 1))
    corr = cov / (std1 * std2)

    return corr


print('R(red, green) = ', getR(imageR, imageG))
print('R(red, blue) = ', getR(imageR, imageB))
print('R(blue, green) = ', getR(imageB, imageG))

yFile = bytearray(fullImage[:pixel_offset])
cbFile = bytearray(fullImage[:pixel_offset])
crFile = bytearray(fullImage[:pixel_offset])

meanY = 0
meanCb = 0
meanCr = 0

yArray = []
cbArray = []
crArray = []
for i in range(pixel_offset, len(fullImage), 3):
    y = 0.299 * fullImage[i + 2] + 0.587 * fullImage[i + 1] + 0.114 * fullImage[i]
    cb = 0.5643 * (fullImage[i] - y) + 128
    cr = 0.7132 * (fullImage[i + 2] - y) + 128
    yArray.append(y)
    cbArray.append(cb)
    crArray.append(cr)
    meanY = meanY + y 
    meanCb = meanCb + cb 
    meanCr = meanCr + cr 
    yFile.extend(bytearray([int(y),int(y),int(y)]))
    crFile.extend(bytearray([int(cr),int(cr),int(cr)]))
    cbFile.extend(bytearray([int(cb),int(cb),int(cb)]))

meanY = meanY / (width * height)
meanCb = meanCb / (width * height)
meanCr = meanCr / (width * height)

stdY = math.sqrt(sum([(yFile[i] - meanY) ** 2 for i in range(0, len(yFile), 3)]) / (width * height - 1))
stdCb = math.sqrt(sum([(cbFile[i] - meanCb) ** 2 for i in range(0, len(cbFile), 3)]) / (width * height - 1))
stdCr = math.sqrt(sum([(crFile[i] - meanCr) ** 2 for i in range(0, len(crFile), 3)]) / (width * height - 1))

covY_Cb = sum([(yFile[i] - meanY) * (crFile[i] - meanCr) for i in range(0, len(yFile), 3)]) / (width * height)
covY_Cr = sum([(yFile[i] - meanY) * (cbFile[i] - meanCb) for i in range(0, len(yFile), 3)]) / (width * height)
covCb_Cr = sum([(cbFile[i] - meanCb) * (crFile[i] - meanCr) for i in range(0, len(yFile), 3)]) / (width * height)
print('--------------------------------------------')
print('R(y, Cb) = ', covY_Cb / (stdY * stdCb))
print('R(y, Cr) = ', covY_Cr / (stdY * stdCr))
print('R(Cb, Cr) = ', covCb_Cr / (stdCr * stdCb))

imageFile = open('y.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()

imageFile = open('Cb.bmp', 'wb')
imageFile.write(bytes(cbFile)) 
imageFile.close()

imageFile = open('Cr.bmp', 'wb')
imageFile.write(bytes(crFile)) 
imageFile.close()

print('--------------------------------------------')
yFile = bytearray(fullImage[:pixel_offset])
sumR = 0
sumG = 0
sumB = 0 
for i in range(len(yArray)):
    g = yArray[i] - 0.714 * (crArray[i] - 128) - 0.334 * (cbArray[i] - 128)
    r = yArray[i] + 1.402 * (crArray[i] - 128)
    b = yArray[i] + 1.772 * (cbArray[i] - 128)
    sumR = sumR + (imageR[i] - r) ** 2
    sumG = sumG + (imageG[i] - g) ** 2
    sumB = sumB + (imageB[i] - b) ** 2 
    yFile.append(int(b))
    yFile.append(int(g))
    yFile.append(int(r))
print('PSNR( Blue ) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumB))
print('PSNR( Green ) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumG))
print('PSNR( Red ) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumR))
imageFile = open('after.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()
import math
import matplotlib.pyplot as plt
import numpy as np
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

with open('kodim02.bmp', 'rb') as f:
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

print('r(red, green) = ', getR(imageR, imageG))
print('r(red, blue) = ', getR(imageR, imageB))
print('r(blue, green) = ', getR(imageB, imageG))

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

stdY = math.sqrt(sum([(yArray[i] - meanY) ** 2 for i in range(0, len(yArray))]) / (width * height - 1))
stdCb = math.sqrt(sum([(cbArray[i] - meanCb) ** 2 for i in range(0, len(cbArray))]) / (width * height - 1))
stdCr = math.sqrt(sum([(crArray[i] - meanCr) ** 2 for i in range(0, len(crArray))]) / (width * height - 1))

covY_Cb = sum([(yArray[i] - meanY) * (crArray[i] - meanCr) for i in range(0, len(yArray))]) / (width * height)
covY_Cr = sum([(yArray[i] - meanY) * (cbArray[i] - meanCb) for i in range(0, len(yArray))]) / (width * height)
covCb_Cr = sum([(cbArray[i] - meanCb) * (crArray[i] - meanCr) for i in range(0, len(yArray))]) / (width * height)
print('--------------------------------------------')
print('r(y, Cb) = ', covY_Cb / (stdY * stdCb))
print('r(y, Cr) = ', covY_Cr / (stdY * stdCr))
print('r(Cb, Cr) = ', covCb_Cr / (stdCr * stdCb))

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
print('psnr(blue) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumB))
print('psnr(green) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumG))
print('psnr(red) = ', 10 * math.log10((width  * height * (255 ** 2)) / sumR))
imageFile = open('after.bmp', 'wb')
imageFile.write(bytes(yFile)) 
imageFile.close()

yArray = [round(yArray[i]) for i in range(len(yArray))]
yArray = np.array(yArray)
cbArray = [round(cbArray[i]) for i in range(len(cbArray))]
cbArray = np.array(cbArray)
crArray = [round(crArray[i]) for i in range(len(crArray))]
crArray = np.array(crArray)

imageR = [round(imageR[i]) for i in range(len(imageR))]
imageR = np.array(imageR)
imageG = [round(imageG[i]) for i in range(len(imageG))]
imageG = np.array(imageG)
imageB = [round(imageB[i]) for i in range(len(imageB))]
imageB = np.array(imageB)


fig = plt.figure()
plt.title("y frequency")
plt.hist(yArray, bins=255)
plt.show()

fig = plt.figure()
plt.title("Cb frequency")
plt.hist(cbArray, bins=255, range=(0,255))
plt.show()

fig = plt.figure()
plt.title("Cr frequency")
plt.hist(crArray, bins=255, range=(0,255))
plt.show()

fig = plt.figure()
plt.title("red frequency")
plt.hist(imageR, bins=255)
plt.show()

fig = plt.figure()
plt.title("green frequency")
plt.hist(imageG, bins=255)
plt.show()

fig = plt.figure()
plt.title("blue frequency")
plt.hist(imageB, bins=255)
plt.show()

print(max(cbArray))
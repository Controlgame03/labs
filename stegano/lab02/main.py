import os
import random
import math

IMAGE_FILENAME = 'lab02/kodim15.bmp'
IMAGE_ENCODED_FILENAME = 'lab02/kodim_encoded.bmp'
TEXT_ORIGIN_FILENAME = 'lab02/text.txt'
TEXT_DECODED_FILENAME = 'lab02/decoded.txt'

PIXEL_OFFSET_CONST = 138
COUNT_BACKUP = 16

TEXT_MASK = 128 # 10000000
IMG_MASK = 254 # 11111110

def generateIndexes(seed, width, height) -> list:
    generatedList = list(range(COUNT_BACKUP, (width * height) * 3))
    random.seed(seed)
   
    return sorted(generatedList, key=lambda x: random.random())

def encrypt(randomKey):
    textFileLen = os.stat(TEXT_ORIGIN_FILENAME).st_size
    imgFileLen = os.stat(IMAGE_FILENAME).st_size
    print(imgFileLen - PIXEL_OFFSET_CONST - COUNT_BACKUP)
    print(textFileLen * 8)
    if textFileLen * 8 > imgFileLen - PIXEL_OFFSET_CONST - COUNT_BACKUP:
        print("Text is too long")
        return

    fullImage, originWidth, originHeight, pixelOffset = getBmpValues(IMAGE_FILENAME)
    indexList = generateIndexes(randomKey, originWidth, originHeight)
    print(len(indexList))
    print(len(fullImage))
    count = 0
    text = open(TEXT_ORIGIN_FILENAME, 'r')
    while True:
        symbol = text.read(1)
        if not symbol:
            break
        currentCharacter = ord(symbol)

        for _ in range(8):
            imgByte = fullImage[pixelOffset + indexList[count]] & IMG_MASK
            encodedByte = imgByte | ((currentCharacter & TEXT_MASK) > 7)

            fullImage[pixelOffset + indexList[count]] = encodedByte

            currentCharacter <<= 1
            count += 1

    
    countBinFormat = f'{count:016b}'
    for i in range(COUNT_BACKUP):
        curBit = 0 if i >= len(countBinFormat) else int(countBinFormat[i])
        imgByte = fullImage[pixelOffset + i] & IMG_MASK
        encodedByte = imgByte | curBit
        fullImage[pixelOffset + i] = encodedByte

    encodedBmpFile = open(IMAGE_ENCODED_FILENAME, 'wb')
    encodedBmpFile.write(fullImage)
    encodedBmpFile.close()
    print(COUNT_BACKUP + count, ' - ', originHeight * originWidth * 3)
    text.close()

def decrypt(key):
    fullImage, originWidth, originHeight, pixelOffset = getBmpValues(IMAGE_ENCODED_FILENAME)
    indexList = generateIndexes(key, originWidth, originHeight)

    count_bit = 0
    for i in range(COUNT_BACKUP):
        imgByte = fullImage[pixelOffset + i] & 1
        count_bit += (2**(COUNT_BACKUP - i - 1)) * imgByte

    count = 0
    textDecrypted = ""
    while count < count_bit:
        symbol = 0
        for _ in range(8):
            symbol <<= 1
            symbol |= fullImage[pixelOffset + indexList[count]] & ~IMG_MASK
            count += 1
        
        textDecrypted += chr(symbol)

    decodedTextFile = open(TEXT_DECODED_FILENAME, 'w')
    decodedTextFile.write(textDecrypted)
    decodedTextFile.close()

def cadr(value):
    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value

def getBmpValues(filename):
    with open(filename, 'rb') as f:
        header = f.read(PIXEL_OFFSET_CONST)
        pixel_offset = int.from_bytes(header[10:14], byteorder='little')
        width = int.from_bytes(header[18:22], byteorder='little')
        height = int.from_bytes(header[22:26], byteorder='little')

        f.seek(0)
        fullImage = bytearray(f.read())

        return bytearray(fullImage), width, height, pixel_offset

def PSNR(originFilename, encodedFilename):
    originFile, originWidth, originHeight, originOffset = getBmpValues(originFilename)
    encodedFile, encodedWidth, encodedHeight, encodedOffset = getBmpValues(encodedFilename)

    originFile = originFile[originOffset:]
    encodedFile = encodedFile[encodedOffset:]

    if originHeight != encodedHeight or originWidth != encodedWidth:
        return
    
    sumR = 0
    sumG = 0
    sumB = 0 
    for i in range(0, len(originFile), 3):
        redId = i + 2
        greenId = i + 1
        blueId = i
        sumR = sumR + (originFile[redId] - encodedFile[redId]) ** 2
        sumG = sumG + (originFile[greenId] - encodedFile[greenId]) ** 2
        sumB = sumB + (originFile[blueId] - encodedFile[blueId]) ** 2 
   
    print('psnr(blue) = ', 10 * math.log10((originWidth  * originHeight * (255 ** 2)) / sumB))
    print('psnr(green) = ', 10 * math.log10((originWidth  * originHeight * (255 ** 2)) / sumG))
    print('psnr(red) = ', 10 * math.log10((originWidth  * originHeight * (255 ** 2)) / sumR))

randomKey = 123
encrypt(randomKey)
decrypt(randomKey)
PSNR(IMAGE_FILENAME, IMAGE_ENCODED_FILENAME)
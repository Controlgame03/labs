import math  
import random

BLOCK_SIZE = 8
WEIGHT_COEF = 1.5
CHANGED_COEF_NUMBER = 2
COUNER_GAP = 16
ENCODED_IMAGE = 'lab03/logs/after.bmp'
ORIGIN_IMAGE = 'lab03/kodim02.bmp'
TEXT_FILE = 'lab03/text.txt'
JPEG_OUTPUT_FILE = 'lab03/logs/file.jpg'
CONVERTED_BMP_FROM_JPEG_FILE = 'lab03/logs/from_jpeg.bmp'
BINARY_ENCODED = 'lab03/logs/encode.txt'
BINARY_DECODED = 'lab03/logs/decode.txt'

def getBmpValues(filename):
    with open(filename, 'rb') as f:
        header = f.read(54)
        pixel_offset = int.from_bytes(header[10:14], byteorder='little')
        width = int.from_bytes(header[18:22], byteorder='little')
        height = int.from_bytes(header[22:26], byteorder='little')

        f.seek(0)
        fullImage = bytearray(f.read())

        return bytearray(fullImage), width, height, pixel_offset
    
def dct(block):
    result = [[0 for _ in range(BLOCK_SIZE)] for _ in range(BLOCK_SIZE)]
    for u in range(8):
        cu = 1 / (2) ** (1/2) if u == 0 else 1
        for v in range(8):
            cv = 1 /(2) ** (1/2) if v == 0 else 1
            sum_val = 0.0
            for i in range(8):
                for j in range(8):
                    sum_val += block[i][j] * math.cos((2 * i + 1) * u * math.pi / 16) * math.cos((2 * j + 1) * v * math.pi / 16)
            result[u][v] = cu * cv * sum_val / 4
    return result

def idct(block):
    result = [[0 for _ in range(BLOCK_SIZE)] for _ in range(BLOCK_SIZE)]

    for i in range(8):
        for j in range(8):
            sum_val = 0.0
            for u in range(8):
                for v in range(8):
                    cu = 1 / (2) ** (1/2) if u == 0 else 1
                    cv = 1 / (2) ** (1/2) if v == 0 else 1
                    sum_val += cu * cv * block[u][v] * math.cos((2 * i + 1) * u * math.pi / 16) * math.cos((2 * j + 1) * v * math.pi / 16)
            result[i][j] = round(sum_val / 4)

    return result

def cadr(value):
    
    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value

def readBinary(filename):
    file = open(filename, "r")
    textValue = file.read()
    file.close()

    return ''.join(format(ord(x), '08b') for x in textValue)

def moveCursor(y, x):
    print("\033[%dD\033[%dA" % (y, x))

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
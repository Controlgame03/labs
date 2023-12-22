from utils import *
import sys

originFile, originWidth, originHeight, originOffset = getBmpValues(ORIGIN_IMAGE)

blockCount = (originHeight * originWidth) // BLOCK_SIZE ** 2

imageComponentMatrix = [] 
greenComponentMatrix = [] 
redComponentMatrix = [] 
for i in range(originOffset, len(originFile), 3):
    imageComponentMatrix.append(originFile[i])
    greenComponentMatrix.append(originFile[i + 1])
    redComponentMatrix.append(originFile[i + 2])


encodedImageBody = bytearray(originFile[:originOffset])

tempStore = [0 for _ in range(originWidth * originHeight)]

encodedText = readBinary(TEXT_FILE)

if len(encodedText) > blockCount:
    print("secret size is greater than the number of blocks")
    sys.exit()

countBinFormat = f'{len(encodedText):016b}'

encodedText = countBinFormat + encodedText

amountPos = 0
textPos = 0
c = 0

for i in range(0, originHeight - BLOCK_SIZE + 1, BLOCK_SIZE):
    for j in range(0, originWidth - BLOCK_SIZE + 1, BLOCK_SIZE):
        
        
        imageBlock = []
        for v in range(BLOCK_SIZE):
            row = []
            for u in range(BLOCK_SIZE):
                row.append(imageComponentMatrix[j + u + (i + v) * originWidth])
                
            imageBlock.append(row)

        dct_result = dct(imageBlock)

        if (textPos < len(encodedText)):
            s = 1 if encodedText[textPos] == '1' else -1
            maxX = []
            maxY = []
            tempMaxArray = []
            for v in range(BLOCK_SIZE):
                for u in range(BLOCK_SIZE):         
                    if not (v == 0 and u == 0):
                        tempMaxArray.append({
                            'value': dct_result[v][u],
                            'x': u,
                            'y': v
                        })
            tempMaxArray = sorted(tempMaxArray, key=lambda x: x['value'], reverse=True)
 
            for coefId in range(CHANGED_COEF_NUMBER):
                newValue = tempMaxArray[coefId]['value'] * (1 + WEIGHT_COEF * s)     
                v = tempMaxArray[coefId]['y']
                u = tempMaxArray[coefId]['x']
                dct_result[v][u] = newValue

            textPos += 1

        idct_result = idct(dct_result)
        
        for v2 in range(BLOCK_SIZE):
            for u2 in range(BLOCK_SIZE):
                tempStore[j + u2 + (i + v2) * originWidth] = cadr(idct_result[v2][u2])

encodedFile = open(BINARY_ENCODED, 'w')
encodedFile.write(encodedText)
encodedFile.close()

for i in range(len(tempStore)):
    encodedImageBody.extend(bytearray([tempStore[i], greenComponentMatrix[i], redComponentMatrix[i]]))

imageFile = open(ENCODED_IMAGE, 'wb')
imageFile.write(bytes(encodedImageBody)) 
imageFile.close()
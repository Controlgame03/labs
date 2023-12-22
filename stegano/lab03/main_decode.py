from utils import *
import sys

encodedImageName = ENCODED_IMAGE

encodedFile, encodedWidth, encodedHeight, encodedOffset = getBmpValues(encodedImageName)
originFile, originWidth, originHeight, originOffset = getBmpValues(ORIGIN_IMAGE)

originImage = []
imageComponentMatrix = [] 

for i in range(encodedOffset, len(encodedFile), 3):
    imageComponentMatrix.append(encodedFile[i])
    originImage.append(originFile[i])

encodedBits = COUNER_GAP

encodedText = ''
encodedCounter = ''
textPos = 0

for i in range(0, encodedHeight - BLOCK_SIZE + 1, BLOCK_SIZE):
    if (textPos >= encodedBits):
        break
    for j in range(0, encodedWidth - BLOCK_SIZE + 1, BLOCK_SIZE):
        originImageBlock = []
        encodedImageBlock = []

        for v in range(BLOCK_SIZE):
            row = []
            originRow = []
            for u in range(BLOCK_SIZE):
                row.append(imageComponentMatrix[j + u + (i + v) * originWidth])
                originRow.append(originImage[j + u + (i + v) * originWidth])
            originImageBlock.append(originRow)
            encodedImageBlock.append(row)

        dct_result = dct(encodedImageBlock)
        dct_result_origin = dct(originImageBlock)
        if (textPos < encodedBits):
            tempMaxValues = []
            tempMaxArray = []
            for v in range(BLOCK_SIZE):
                for u in range(BLOCK_SIZE):
                    if not (v == 0 and u == 0):
                        tempMaxArray.append({
                            'value': dct_result_origin[v][u],
                            'x': u,
                            'y': v
                        })
            tempMaxArray = sorted(tempMaxArray, key=lambda x: x['value'], reverse=True)
            for coefId in range(CHANGED_COEF_NUMBER):
                v = tempMaxArray[coefId]['y']
                u = tempMaxArray[coefId]['x']

                x = (abs(dct_result_origin[v][u]) - abs(dct_result[v][u]))
                tempMaxValues.append(1 if x < 0 else 0)

            bitValue = str(round(sum(tempMaxValues) / len(tempMaxValues)))
            encodedText += bitValue
            textPos += 1
            if len(encodedCounter) < COUNER_GAP:
                encodedCounter += bitValue
                if len(encodedCounter) == COUNER_GAP:
                    for numId in range(COUNER_GAP):
                        encodedBits += (2**(COUNER_GAP - numId - 1)) * int(encodedCounter[numId])
        else:
            break

encodedFile = open(BINARY_DECODED, 'w')
encodedFile.write(encodedText)
encodedFile.close()
result = ""
byteLength = 8
encodedText = encodedText[COUNER_GAP:]
for i in range(len(encodedText) // byteLength):
   start = i * byteLength
   end = start + byteLength
   result += chr(int(encodedText[start : end], 2))
print(result)
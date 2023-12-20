from utils import *

originFile, originWidth, originHeight, originOffset = getBmpValues(ORIGIN_IMAGE)

imageComponentMatrix = [] 
greenComponentMatrix = [] 
redComponentMatrix = [] 
for i in range(originOffset, len(originFile), 3):
    imageComponentMatrix.append(originFile[i])
    greenComponentMatrix.append(originFile[i + 1])
    redComponentMatrix.append(originFile[i + 2])

tempStore = [0 for _ in range(originWidth * originHeight)]

for i in range(0, originHeight - BLOCK_SIZE + 1, BLOCK_SIZE):
    for j in range(0, originWidth - BLOCK_SIZE + 1, BLOCK_SIZE):
        imageBlock = []
        
        for v in range(BLOCK_SIZE):
            row = []
            for u in range(BLOCK_SIZE):
                row.append(imageComponentMatrix[j + u + (i + v) * originWidth])
                
            imageBlock.append(row)

        dct_result = dct(imageBlock)
        idct_result = idct(dct_result)

        for v2 in range(BLOCK_SIZE):
            for u2 in range(BLOCK_SIZE):
                tempStore[j + u2 + (i + v2) * originWidth] = cadr(idct_result[v2][u2])

encodedImageBody = bytearray(originFile[:originOffset])
for i in range(len(tempStore)):
    encodedImageBody.extend(bytearray([tempStore[i], greenComponentMatrix[i], redComponentMatrix[i]]))

imageFile = open('test.bmp', 'wb')
imageFile.write(bytes(encodedImageBody)) 
imageFile.close()
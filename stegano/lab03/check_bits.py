from utils import *

encodedFile = open(BINARY_ENCODED, 'r')
decodedFile = open(BINARY_DECODED, 'r')

origin  = encodedFile.readline().strip()
encoded = decodedFile.readline().strip()

count = 0

logFile = open('lab03/logs/difference.txt', 'w')

for i in range(min(len(origin), len(encoded))):
    if origin[i] != encoded[i]:
        logFile.write(str(i) + ' ' + str(origin[i]) + ' - ' + str(encoded[i]) + '\n')
        count += 1

logFile.write(str(count) + ' from ' + str(len(origin)) + '\n')
logFile.write('Difference in bits: ' + str(len(origin) - len(encoded)) + '\n')
logFile.close()

PSNR(ORIGIN_IMAGE, ENCODED_IMAGE)
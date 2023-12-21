import random

import bitarray as bitarray
from PIL import Image
import numpy as np

img = Image.open('test_image.bmp')

secret = bitarray.bitarray()
secret.frombytes(open('secret.txt', 'r').read().encode('utf-8'))

w = img.width
h = img.height

size = w * h

blocksize = size // len(secret)
if not blocksize:
    blocksize = size
open('bs.txt', 'w').write(str(blocksize))

imgarray = np.array(img)

def generatekey(l):
    ret = [i for i in range(l)]
    random.shuffle(ret)
    return ret

def getLSB(a):
    if a % 2 == 0:
        return 0
    else:
        return 1

blocks = [i for i in range(0, len(secret) * blocksize, blocksize)]

key = generatekey(len(secret))
open('key.txt', 'w').write(' '.join(list(map(str, key))))

blocks = [blocks[i] for i in key]
sidx = 0

for block in blocks:
    #вычислить значение lsb для этого блока
    total_sum = 0
    for k in range(block, block + blocksize):
        total_sum += getLSB(imgarray[(k - (k % w)) // w][k % w][0])
    total_sum = getLSB(total_sum)
    if total_sum != secret[sidx]:
        j = block % w
        i = (block - j) // w
        imgarray[i][j][0] += 1 if imgarray[i][j][0] % 2 == 0 else -1
    sidx += 1

hideimg = Image.fromarray(imgarray)

hideimg.save('secret_image.bmp')
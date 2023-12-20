import random

import bitarray as bitarray
from PIL import Image
import numpy as np

img = Image.open('pic.bmp')

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
    b = getLSB(sum([getLSB(imgarray[(k - (k % h)) // h][k % h][0]) for k in range(block, block + blocksize)]))
    if b != secret[sidx]:
        j = block % h
        i = (block - j) // h
        imgarray[i][j][0] += 1 if imgarray[i][j][0] % 2 == 0 else -1
    sidx += 1

hideimg = Image.fromarray(imgarray)

hideimg.save('hidepic.bmp')
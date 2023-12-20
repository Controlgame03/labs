from PIL import Image
import numpy as np

hideimg = Image.open('hidepic.bmp')

w = hideimg.width
h = hideimg.height

size = w * h

#blocksize = int(open('bs.txt', 'r').readline())
blocksize = int(input('Enter size of block: '))

imgarray = np.array(hideimg)

key = open('key.txt', 'r').readline().split(' ')
key = [int(i) for i in key]

def getLSB(a):
    if a % 2 == 0:
        return 0
    else:
        return 1

blocks = [i for i in range(0, size, blocksize)]
blocks = [blocks[i] for i in key]

secretbits = []
secret = ''

for block in blocks:
    b = getLSB(sum([getLSB(imgarray[(k - (k % h)) // h][k % h][0]) for k in range(block, block + blocksize)]))
    secretbits.append(b)


for i in range(0, len(secretbits), 8):
    s = secretbits[i:i+8]
    s = '0b'+''.join(list(map(str, s)))
    secret += chr(int(s, 2))

print(f'Your secret: {secret}')
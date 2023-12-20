TEXT_ORIGIN_FILENAME = 'lab02/text.txt'

textDecrypted = ''
for i in range(int(147454*0.05)):
    textDecrypted += 'a'
decodedTextFile = open(TEXT_ORIGIN_FILENAME, 'w')
decodedTextFile.write(textDecrypted)
decodedTextFile.close()
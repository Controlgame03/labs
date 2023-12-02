ruSymbolList = ['А','а','Е','е','Т','О','о','Р','р','Н','К','Х','х','В','М','С','с','у']
enSymbolList = ['A','a','E','e','T','O','o','P','p','H','K','X','x','B','M','C','c','y']

def readBinary(filename):
    file = open(filename, "r")
    textValue = file.read()
    file.close()

    return ''.join(format(ord(x), '08b') for x in textValue)

def encodeText(containerFilename, valueFalename, stegContainerFilename):
    
    containerCharacterList = []
    with open(containerFilename, 'r', encoding='utf-8') as file:
        while True:
            char = file.read(1)
            containerCharacterList.append(char)
            if not char:
                break

    str = readBinary(valueFalename)
    textLength = len(str)
    count = 0
    print('secret length: ', textLength)
    print('text length: ', len(containerCharacterList))
    for i in range(len(containerCharacterList)):
        if count >= textLength:
            break

        if containerCharacterList[i] in ruSymbolList:
            symbolId = ruSymbolList.index(containerCharacterList[i])
            if str[count] == '1':
                containerCharacterList[i] = enSymbolList[symbolId]
            count += 1
                
    print(count)
    with open(stegContainerFilename, "w") as output:
        output.write(''.join(containerCharacterList))

    return count

def decodeText(stegContainerFilename, bits):
    count = 0
    encodedBinaryValue = ""

    with open(stegContainerFilename, 'r') as file:
        while True:
            ascii = file.read(1)
            if count < bits:
                for i in range(len(ruSymbolList)):
                    if ascii == ruSymbolList[i]:
                        encodedBinaryValue += '0'
                        count += 1
                    elif ascii == enSymbolList[i]:
                        encodedBinaryValue += '1'
                        count += 1
            if not ascii:
                break
    
    result = ""
    byteLength = 8
    for i in range(len(encodedBinaryValue) // byteLength):
       start = i * byteLength
       end = start + byteLength

       result += chr(int(encodedBinaryValue[start : end], 2))
    return result

containerFilename = 'container.txt'
stegContainerFilename = 'steg-container.txt'
valueFalename = 'text.txt'

bitCounter = encodeText(containerFilename, valueFalename, stegContainerFilename)
decodeResult = decodeText(stegContainerFilename, bitCounter)

print(decodeResult)
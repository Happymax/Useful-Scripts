import math

print("==== Cache Calculator ====")
print("n-way Set-Associative Mode")
n = int(input("n = "))
cacheSize = int(input("Cache Size (Bytes) = "))
cacheLineSize = int(input("Size of Cache Line (Bytes) = "))
if ((n <= 0) | (cacheSize <= 0) | (cacheLineSize <= 0)
        | (cacheSize % cacheLineSize != 0) | ((cacheSize // cacheLineSize) % n != 0)):
    print("Wrong values provided!")
    exit(1)
lineCount = cacheSize // cacheLineSize
print("Number of Cache Lines: " + str(lineCount))
setCount = lineCount // n
print("Number of Sets: " + str(setCount))
indexBitWidth = math.ceil(math.log2(setCount))
print("Index Bit Width: " + str(indexBitWidth) + " Bits")
offsetBitWidth = math.ceil(math.log2(cacheLineSize))
print("Offset Bit Width: " + str(offsetBitWidth) + " Bits")
print("==== Initialization Complete ====")
print("Input Address (in Hex) to Calculate or 'q' to Quit")
while True:
    print("--------------------")
    i = input()
    if (i[0] == 'q') | (i[0] == 'Q'):
        exit(0)
    try:
        address = int(i, 16)
    except ValueError:
        print("Not a address!")
        continue
    blockNumber = address // cacheLineSize
    print("Block Number: " + hex(blockNumber))
    index = blockNumber % setCount
    print("Set Index: " + hex(index))
    tag = address >> (indexBitWidth + offsetBitWidth)
    print("Tag: " + hex(tag))

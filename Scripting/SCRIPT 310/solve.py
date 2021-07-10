import binascii

f = open('flag.txt', 'rb')

content = f.read()
print(f"Content: {content}")
print("-----------------------")

hex_flag = binascii.hexlify(content).decode()
print(f"Hex: {hex_flag}")
print("-----------------------")

binary = hex_flag.replace('0a', '0').replace('0d', '1')
print(f"Binary: {binary}")
print("-----------------------")

# convert every 8 bits (1 byte) into a character
characters = []
for i in range(len(binary)//8): 
    bin2int = int(binary[ i*8 : i*8+8 ], 2)
    int2char = chr(bin2int)
    characters.append(int2char)
print(f"List of characters: {characters}")
print("-----------------------")

flag = "".join(characters)
 
print(flag)
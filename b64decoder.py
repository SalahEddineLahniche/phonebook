import sys
from base64 import b64decode as decode

print("Write the base 64 code then press EOF (CTRL + Z):")
string = sys.stdin.read()
string = string.replace(" ", "")
string = string.replace("\n", "")

bytes_array = decode(string)

print("choose a filename:", end="")
filename = input()
file = open(filename, "wb")
file.write(bytes_array)
file.close()

import sys
from pathlib import Path
from tkinter import filedialog as fd
import tkinter as tk
from time import time
sys.path.insert(1, str(Path(__file__).resolve().parent.parent) + "\\src")
import biteasy
file = fd.askopenfilename()
start = time()
fileread = biteasy.readfrom.file(file)
end = time()
print("time took to read file: " + str(end - start))
def inttest():
    start = time()
    print("File read Using module (unsigned): " + str(fileread.readbits(0, 8).ConvertToInt(False)))
    end = time()
    print("Time took: " + str(end - start))
    start = time()
    print("File read Using module (signed): " + str(fileread.readbits(0, 8).ConvertToInt(True)))
    end = time()
    print("Time took: " + str(end - start))
    start = time()
    with open(file, "rb") as f:
        bytes = f.read()
    print("File read not using module: " + str(int.from_bytes(bytes[0:1], "big")))
    end = time()
    print("Time took: " + str(end - start))
    if int.from_bytes(bytes[0:1], "big") == fileread.readbits(0, 8).ConvertToInt():
        print("Test 2 Passed (intiger)")
    else:
        print("Test 2 did not pass (intiger)")
def bytestest():
    start = time()
    print("File read Using module: " + str(fileread.readbits(0, 32).ConvertToBytes()))
    end = time()
    print("Time took: " + str(end - start))
    start = time()
    with open(file, "rb") as f:
        bytes = f.read()
    print("File read not using module: " + str(bytes[0:4]))
    end = time()
    print("Time took: " + str(end - start))
    if bytes[0:4] == fileread.readbits(0, 32).ConvertToBytes():
        print("Test 3 Passed (bytes)")
    else:
        print("Test 3 did not pass (bytes)")
def stringtest():
    start = time()
    print("File read Using module: " + fileread.readbits(0, 32).ConvertToStr())
    end = time()
    print("Time took: " + str(end - start))
    start = time()
    with open(file, "rb") as f:
        bytes = f.read()
    print("File read not using module: " + str(bytes[0:4], "UTF-8"))
    end = time()
    print("Time took: " + str(end - start))
    if str(bytes[0:4], "UTF-8") == fileread.readbits(0, 32).ConvertToStr():
        print("Test 4 Passed (string)")
    else:
        print("Test 4 did not pass (string)")
def main():
    inttest()
    bytestest()
    stringtest()
if __name__ == "__main__":
    main()
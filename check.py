import sys
import os

with open("debug/logging.log") as f:
    print(f.read())

if input("prof (y;n) : ") == "y":
    import debug.get

#if input("cython (y;n) : ") == "y":
#    with open("mainloop/blit/blit.cpython-313.so", "rb") as file:
#        print(file.read())
from setuptools import setup
from Cython.Build import cythonize
from os import getcwd, system

print("cython : ", getcwd())
path = "MyGood_Pyfile/潛執的囚禁/"

if __name__ == "__main__":
    path = ""

# /storage/emulated/0/

setup(
    ext_modules=cythonize([
        f"{path}mainloop/blit/blit.py", 
        f"{path}mainloop/stop/run.py", 
        f"{path}mainloop/loop/catch.py"
    ],
    language_level=3,
    compiler_directives={
        "boundscheck": False,
        "wraparound": False,
        "cdivision": True,
    })
)

# bash : python MyGood_Pyfile/潜执の囚禁/setup.py build_ext --inplace

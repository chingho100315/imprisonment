import pygame
import logging
import sys

logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s\n%(levelname)s\n%(message)s\n", 
    handlers=[
        logging.FileHandler("debug/logging.log")
    ]
)

try:
    with open("main.py", "r") as file:
        exec(file.read())
except Exception as error:
    logging.error(error)
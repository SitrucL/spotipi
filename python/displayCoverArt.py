import configparser
import logging
import os
from io import BytesIO
from logging.handlers import RotatingFileHandler

import requests
import socketio
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Setup sockets
sio = socketio.Client()
sio.connect('https://personal-spotify-handler.fly.dev')
# sio.connect("http://192.168.1.31:8080")

# Configuration file
dir = os.path.dirname(__file__)
filename = os.path.join(dir, "../config/rgb_options.ini")

# Configures logger for storing song data
logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filename="spotipy.log",
    level=logging.INFO,
)
logger = logging.getLogger("spotipy_logger")

# automatically deletes logs more than 2000 bytes
handler = RotatingFileHandler("spotipy.log", maxBytes=2000, backupCount=3)
logger.addHandler(handler)

# Configuration for the matrix
config = configparser.ConfigParser()
config.read(filename)

options = RGBMatrixOptions()
options.rows = int(config["DEFAULT"]["rows"])
options.cols = int(config["DEFAULT"]["columns"])
options.chain_length = int(config["DEFAULT"]["chain_length"])
options.parallel = int(config["DEFAULT"]["parallel"])
options.hardware_mapping = config["DEFAULT"]["hardware_mapping"]
options.gpio_slowdown = int(config["DEFAULT"]["gpio_slowdown"])
options.panel_type = config["DEFAULT"]["panel_type"]
options.brightness = int(config["DEFAULT"]["brightness"])
options.limit_refresh_rate_hz = int(config["DEFAULT"]["refresh_rate"])

default_image = os.path.join(dir, config["DEFAULT"]["default_image"])
print(default_image)
matrix = RGBMatrix(options=options)


@sio.on("track_data")
def on_message(data):

    print(data["currentlyPlaying"]["images"][0]["url"])
    try:

        imageURL = data["currentlyPlaying"]["images"][0]["url"]
        response = requests.get(imageURL)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert("RGB"))

    except Exception as e:
        image = Image.open(default_image)
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert("RGB"))
        print(e)

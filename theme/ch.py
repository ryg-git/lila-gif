#!/usr/bin/env python3

from chess.svg import SQUARE_SIZE

import io
import subprocess
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import importlib

ms = importlib.import_module("make-sprites")

NONTHEME_COLORS = [
    "#262421",  # dark background
    "#bababa",  # text color
    "#bf811d",  # title color
    "#b72fc6",  # bot color
    "#706f6e",  # 50% text color on dark background
]

PIECE_SETS = [
    "alpha",
    "anarcandy",
    "caliente",
    "california",
    "cardinal",
    "cburnett",
    "celtic",
    "chess7",
    "chessnut",
    "cooke",
    "companion",
    "disguised",
    "dubrovny",
    "fantasy",
    "fresca",
    "gioco",
    "governor",
    "horsey",
    "icpieces",
    "kiwen-suwi",
    "kosal",
    "leipzig",
    "letter",
    "libra",
    "maestro",
    "merida",
    "monarchy",
    "mpchess",
    "pirouetti",
    "pixel",
    "reillycraig",
    "riohacha",
    "shapes",
    "spatial",
    "staunty",
    "tatiana",
]

COLOR_WIDTH = SQUARE_SIZE * 2 // 3

def resvg(path):
    res = subprocess.run(
        ["resvg", path, "-c", "-w", "90"],
        stdout=subprocess.PIPE,
    )

    return Image.open(io.BytesIO(res.stdout), formats=["PNG"])

def resvg_pieces(piece_set):
    print(f"Preparing {piece_set} pieces...")
    return {f"{color}{piece}": resvg(f"piece/{piece_set}/{color}{piece}.svg") for color in "wb" for piece in "PNBRQK"}

def make_ch_sprite(piece_set_name: str):
    image = Image.new("RGB", (8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
    draw = ImageDraw.Draw(image, "RGBA")

    for y in range(2, 6):
        for x in range(8):
            rect = (x * SQUARE_SIZE, 0, (x + 1) * SQUARE_SIZE - 1, SQUARE_SIZE * 8 - 1)
            draw.rectangle(rect, fill=NONTHEME_COLORS[0])


    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")

    print(f"sprites/crazyhouse-{piece_set_name}.gif")

    return image.quantize(64, dither=0)

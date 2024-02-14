#!/usr/bin/env python3

from chess.svg import SQUARE_SIZE
from PIL import Image

import io
import subprocess
import xml.etree.ElementTree as ET
import importlib

ms = importlib.import_module("make-sprites")


def make_ch_sprite(piece_set_name: str):
    svg = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "version": "1.1",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "viewBox": f"0 0 {SQUARE_SIZE * 8} {SQUARE_SIZE * 8}",
        },
    )

    defs = ET.SubElement(svg, "defs")

    for g in ms.make_piece_set(piece_set_name):
        defs.append(ET.fromstring(g))

    for y in range(5):
        for x in range(8):
            ET.SubElement(
                svg,
                "rect",
                {
                    "x": str(SQUARE_SIZE * x),
                    "y": str(SQUARE_SIZE * y),
                    "width": str(SQUARE_SIZE),
                    "height": str(SQUARE_SIZE),
                    "stroke": "none",
                    "fill": "#888888",
                },
            )

            color = "w" if x >= 4 else "b"

            if y == 0:
                ET.SubElement(
                    svg,
                    "use",
                    {
                        "xlink:href": f"#{color}{ms.PIECE_TYPES[1 + x % 4]}",
                        "transform": f"translate({SQUARE_SIZE * x}, 0)",
                        "opacity": "0.1",
                    },
                )

            else:
                ET.SubElement(
                    svg,
                    "use",
                    {
                        "xlink:href": f"#{color}{ms.PIECE_TYPES[1 + x % 4]}",
                        "transform": f"translate({SQUARE_SIZE * x}, {SQUARE_SIZE * y})",
                    },
                )

                ET.SubElement(
                    svg,
                    "image",
                    {
                        "xlink:href": f"ch-numbers/ch{y}.png",
                        "transform": f"translate({SQUARE_SIZE * (x + 0.60)}, {SQUARE_SIZE * (y + 0.60)})",
                        "width": "15",
                        "height": "15"
                    },
                )

    for x in range(8):
        ET.SubElement(
            svg,
            "rect",
            {
                "x": str(SQUARE_SIZE * x),
                "y": str(SQUARE_SIZE * 5),
                "width": str(SQUARE_SIZE),
                "height": str(SQUARE_SIZE),
                "stroke": "none",
                "fill": "#888888",
            },
        )

        color = "w" if x >= 4 else "b"

        ET.SubElement(
            svg,
            "use",
            {
                "xlink:href": f"#{color}{ms.PIECE_TYPES[0]}",
                "transform": f"translate({SQUARE_SIZE * x}, {SQUARE_SIZE * 5})",
                "opacity": "0.1",
            },
        )

    for y in range(6, 8):
        for x in range(8):
            ET.SubElement(
                svg,
                "rect",
                {
                    "x": str(SQUARE_SIZE * x),
                    "y": str(SQUARE_SIZE * y),
                    "width": str(SQUARE_SIZE),
                    "height": str(SQUARE_SIZE),
                    "stroke": "none",
                    "fill": "#888888",
                },
            )

            color = "w" if y == 7 else "b"

            ET.SubElement(
                svg,
                "use",
                {
                    "xlink:href": f"#{color}{ms.PIECE_TYPES[0]}",
                    "transform": f"translate({SQUARE_SIZE * x}, {SQUARE_SIZE * y})",
                },
            )

            ET.SubElement(
                svg,
                "image",
                {
                    "xlink:href": f"ch-numbers/ch{x + 1}.png",
                    "transform": f"translate({SQUARE_SIZE * (x + 0.60)}, {SQUARE_SIZE * (y + 0.60)})",
                    "width": "15",
                    "height": "15"
                },
            )

    resvg = subprocess.run(
        "resvg --resources-dir . --zoom 2 - -c",
        shell=True,
        input=ET.tostring(svg),
        capture_output=True,
    )

    image = Image.open(io.BytesIO(resvg.stdout), formats=[
                       "PNG"]).quantize(64, dither=0)

    print(f"sprites/crazyhouse-{piece_set_name}.gif")

    image.save(
        f"sprites/crazyhouse-{piece_set_name}.gif", optimize=True, interlace=False
    )

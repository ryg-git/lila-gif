#!/usr/bin/env python3

import subprocess
import io
from PIL import Image, ImageDraw


SQUARE_SIZE = 90

HIGHLIGHT = "#9bc70069"

BOARD_THEMES = {
    "blue":   ("#dee3e6", "#8ca2ad"),
    "brown":  ("#f0d9b5", "#b58863"),
    "green":  ("#ffffdd", "#86a666"),
    "ic":     ("#ececec", "#c1c18e"),
    "pink":   ("#f1f1c9", "#f07272"),
    "purple": ("#9f90b0", "#7d4a8d"),
}

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

NONTHEME_COLORS = [
    "#262421",   # dark background
    "#bababa",   # text color
    "#bf811d",   # title color
    "#b72fc6",   # bot color
    "#706f6e",   # 50% text color on dark background
    "#ffffff00", # transparency
]


def resvg(path):
    res = subprocess.run(
        ["resvg", path, "-c", "-w", "90"],
        stdout=subprocess.PIPE,
# Ensure that the ids of all elements are unique by prefixing with the name of the piece
# Can be done with SVGO prefixIds instead
def namespace_ids(element: ET.Element, piece: str):
    prefix = piece + "-"
    if element.get("id"):
        element.set("id", prefix + element.get("id"))
    for key, value in element.attrib.items():
        id_index = value.find("url(#")
        if id_index >= 0:
            element.set(key, value[0 : id_index + 5] + prefix + value[id_index + 5 :])
        elif key.endswith("href") and value.startswith("#"):
            element.set(key, "#" + prefix + element.get(key)[1:])
    for child in element:
        namespace_ids(child, piece)


# Ensure that the class names of all elements are unique by prefixing with the name of the piece
# Can be done with SVGO prefixIds instead
def namespace_classnames(element: ET.Element, piece: str):
    prefix = piece + "-"
    if element.get("class"):
        element.set(
            "class",
            " ".join(
                [prefix + classname for classname in element.get("class").split(" ")]
            ),
        )
    # For any style tags like:
    # <style>.st0{fill:none}.st1{fill:#010101}.st2{fill:#6d6e6e}</style>
    # Include a piece prefix in front of every class name:
    # <style>.bB-st0{fill:none}.bB-st1{fill:#010101}.bB-st2{fill:#6d6e6e}</style>
    if element.tag.endswith("style"):
        element.text = re.sub(r"\.(.*?)\{", r"." + prefix + r"\1{", element.text)
    for child in element:
        namespace_classnames(child, piece)


piece_sets = {}


def make_piece_set(piece_set_name: str):
    if piece_sets.get(piece_set_name):
        return piece_sets[piece_set_name]

    piece_set = []
    for piece in PIECES:
        svg = ET.parse(f"piece/{piece_set_name}/{piece}.svg")

        root = svg.getroot()
        resize_svg_root(root)

        # TODO: run SVGO with the prefixIds plugin on all SVGs so we don't have to do the following
        namespace_ids(root, piece)
        namespace_classnames(root, piece)

        root.attrib["id"] = piece
        piece_set.append(ET.tostring(root, "utf8", method="xml"))

    piece_sets[piece_set_name] = piece_set
    return piece_set


def make_sprite(theme_name: str, piece_set_name: str):
    svg = ET.Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "version": "1.1",
            "xmlns:xlink": "http://www.w3.org/1999/xlink",
            "viewBox": f"0 0 {SQUARE_SIZE * 8} {SQUARE_SIZE * 9}",
        },
    )

    return Image.open(io.BytesIO(res.stdout), formats=["PNG"])

def resvg_pieces(piece_set):
    print(f"Preparing {piece_set} pieces...")
    return {f"{color}{piece}": resvg(f"piece/{piece_set}/{color}{piece}.svg") for color in "wb" for piece in "PNBRQK"}

def make_sprite(light, dark, pieces, check_gradient):
    image = Image.new("RGB", (8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
    draw = ImageDraw.Draw(image, "RGBA")

    for x in range(8):
        # Background
        fill = light if x % 2 == 0 else dark
        rect = (x * SQUARE_SIZE, 0, (x + 1) * SQUARE_SIZE - 1, SQUARE_SIZE * 8 - 1)
        draw.rectangle(rect, fill=fill)
        if x in [2, 3, 6, 7]:
            draw.rectangle(rect, fill=HIGHLIGHT)

        # Pieces
        color = "b" if x < 4 else "w"
        for i, piece in enumerate("PNBRQKK"):
            y = i + 1
            pos = (x * SQUARE_SIZE, y * SQUARE_SIZE)

            if y == 7:
                image.paste(check_gradient, pos, check_gradient)

            piece = pieces[f"{color}{piece}"]
            image.paste(piece, pos, piece)

    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    for x in range(8):
        ET.SubElement(
            svg,
            "rect",
            {
                "x": str(SQUARE_SIZE * x),
                "y": str(SQUARE_SIZE * 8),
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
                "xlink:href": f"#{color}{PIECE_TYPES[min(x, 6) - 1]}",
                "transform": f"translate({SQUARE_SIZE * x}, {SQUARE_SIZE * 8})",
                "opacity": "0.3",
            },
        )

    resvg = subprocess.run(
        "resvg --resources-dir . --zoom 2 - -c",
        shell=True,
        input=ET.tostring(svg),
        capture_output=True,
    )

    for i, color in enumerate(NONTHEME_COLORS):
        width = 4 * SQUARE_SIZE / len(NONTHEME_COLORS)
        draw.rectangle((4 * SQUARE_SIZE + i * width, 0, 4 * SQUARE_SIZE + (i + 1) * width - 1, SQUARE_SIZE - 1), fill=color)

    return image.quantize(64, dither=0)

def main():
    check_gradient = resvg("check-gradient.svg")
    piece_sets = {piece_set: resvg_pieces(piece_set) for piece_set in PIECE_SETS}

    for board_theme, (light, dark) in BOARD_THEMES.items():
        print(f"Generating sprites for {board_theme}...")
        for piece_set, pieces in piece_sets.items():
            image = make_sprite(light=light, dark=dark, pieces=pieces, check_gradient=check_gradient)
            image.save(f"sprites/{board_theme}-{piece_set}.gif", optimize=True, interlace=False, transparency=image.getpixel((SQUARE_SIZE * 8 - 1, 0)))
def make_crazyhouse_sprite(piece_set_name):
    from ch import make_ch_sprite
    make_ch_sprite(piece_set_name)

def make_all_sprites():
    for piece_set_name in get_piece_set_names():
        for theme_name in THEMES.keys():
            make_sprite(theme_name, piece_set_name)

        make_crazyhouse_sprite(piece_set_name)


if __name__ == "__main__":
    main()

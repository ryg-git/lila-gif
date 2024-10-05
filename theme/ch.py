#!/usr/bin/env python3

from PIL import Image, ImageDraw

SQUARE_SIZE = 90

def make_ch_sprite(pieces, ch_nums):
    image = Image.new("RGB", (8 * SQUARE_SIZE, 8 * SQUARE_SIZE))
    draw = ImageDraw.Draw(image, "RGBA")

    fill = "#262421"

    rect = (0, 0, 8 * SQUARE_SIZE, 8 * SQUARE_SIZE)

    draw.rectangle(rect, fill=fill)

    for y in range(5):
        for i, piece in enumerate("NBRQ"):
            wpos = (i * SQUARE_SIZE, y * SQUARE_SIZE)
            wpiece = pieces[f"w{piece}"]
            image.paste(wpiece, wpos, wpiece)

            bpos = ((4 + i) * SQUARE_SIZE, y * SQUARE_SIZE)
            bpiece = pieces[f"b{piece}"]
            image.paste(bpiece, bpos, bpiece)
    
    # for y in range(1, 5):
    #     for x in range(8):
    #         pos = (x * SQUARE_SIZE + 5, y * SQUARE_SIZE + 5)
    #         num = ch_nums[x + 1]
    #         image.paste(num, pos, num)

    wpos = (i * SQUARE_SIZE, y * SQUARE_SIZE)
    wpiece = pieces[f"w{piece}"]
    image.paste(wpiece, wpos, wpiece)

    for x in range(4):
        pos = (x * SQUARE_SIZE, 5 * SQUARE_SIZE)
        piece = pieces["wP"]
        image.paste(piece, pos, piece)

    for x in range(4, 8):
        pos = (x * SQUARE_SIZE, 5 * SQUARE_SIZE)
        piece = pieces["bP"]
        image.paste(piece, pos, piece)

    for x in range(8):
        wpos = (x * SQUARE_SIZE, 6 * SQUARE_SIZE)
        wpiece = pieces[f"wP"]
        image.paste(wpiece, wpos, wpiece)

        bpos = (x * SQUARE_SIZE, 7 * SQUARE_SIZE)
        bpiece = pieces[f"bP"]
        image.paste(bpiece, bpos, bpiece)

    draw.rectangle((0, 0, 8 * SQUARE_SIZE, SQUARE_SIZE),
                   fill="#262421AA")

    draw.rectangle((0, 5 * SQUARE_SIZE, 8 * SQUARE_SIZE, 6 * SQUARE_SIZE),
                   fill="#262421AA")

    image = image.convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")

    return image.quantize(64, dither=0)

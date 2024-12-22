import math
import random
from colorsys import hsv_to_rgb, rgb_to_hsv

from jelka import Jelka
from jelka.shapes import Plane
from jelka.types import Color

c1: Color
c2: Color


def callback(jelka: Jelka):
    global c1, c2

    plane = Plane(jelka.center_normalized, (math.sin(jelka.frame / 40), 0, math.cos(jelka.frame / 40)))
    threshold = 0.1

    if jelka.frame % 150 == 0:
        c1 = Color.random().vivid()
        c1hsv = rgb_to_hsv(c1.red / 255.0, c1.green / 255.9, c1.green / 255.0)
        c2hsv = ((c1hsv[0] * 360 + random.randint(100, 200) % 360) / 360.0, c1hsv[1], c1hsv[2])
        conv = hsv_to_rgb(*c2hsv)
        c2 = Color(conv[0] * 255, conv[1] * 255, conv[2] * 255).vivid()

    for light, position in jelka.positions_normalized.items():
        dcrtica = position.dot(plane.normal)

        if plane.d - threshold <= dcrtica <= plane.d + threshold:
            jelka.set_light(light, c1)
        else:
            jelka.set_light(light, c2)


def main():
    jelka = Jelka(60)
    jelka.run(callback)


main()

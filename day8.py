import os
import collections
from dataclasses import dataclass, field
from typing import List, DefaultDict

Dimensions = collections.namedtuple("Dimensions", ["w", "h"])


@dataclass
class Layer:

    rows: List[List[int]]
    counts: DefaultDict[int, int] = field(
        default_factory=lambda: collections.defaultdict(int)
    )

    def __post_init__(self) -> None:
        for row in self.rows:
            for pixel in row:
                self.counts[pixel] += 1


def parse_layers(pixels: List[int], dimensions: Dimensions) -> List[Layer]:

    layers: List[Layer] = []

    while pixels:
        layer_pixels: List[List[int]] = []
        for _ in range(dimensions.h):
            layer_pixels.append(pixels[: dimensions.w])
            pixels = pixels[dimensions.w :]
        layers.append(Layer(layer_pixels))

    return layers


if __name__ == "__main__":

    with open(os.path.join("inputs", "day8.in")) as f:
        pixels = [int(pixel) for pixel in f.read().strip()]

    layers = parse_layers(pixels, Dimensions(25, 6))

    # First part
    fewest_zeroes = min(layers, key=lambda layer: layer.counts[0])
    assert fewest_zeroes.counts[1] * fewest_zeroes.counts[2] == 1703

    # Second part
    composite: List[List[int]] = layers[-1].rows

    for layer in reversed(layers[:-1]):
        for y in range(len(layer.rows)):
            for x in range(len(layer.rows[y])):
                pixel = layer.rows[y][x]
                # Ignore transparent pixels
                if pixel != 2:
                    composite[y][x] = pixel

    pixel_map = {1: "*", 0: " "}
    for row in composite:
        print(" ".join(pixel_map[pixel] for pixel in row))

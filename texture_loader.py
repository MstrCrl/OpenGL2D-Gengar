import numpy as np

COLOR_MAP = {
    "A": (149/255, 186/255, 255/255),
    "B": (27/255, 44/255, 90/255),
    "C": (76/255, 172/255, 118/255),
    "D": (153/255, 217/255, 77/255),
    "E": (7/255, 5/255, 18/255),
    "F": (152/255, 100/255, 208/255),
    "G": (24/255, 26/255, 77/255),
    "H": (255/255, 203/255, 91/255),
    "I": (206/255, 123/255, 89/255),
    "J": (250/255, 252/255, 212/255),
    "K": (100/255, 145/255, 210/255),
    "L": (129/255, 60/255, 84/255),
    "M": (244/255, 199/255, 192/255),
    "N": (66/255, 33/255, 116/255),
    "O": (24/255, 6/255, 51/255),
    "P": (14/255, 33/255, 64/255),
    "Q": (228/255, 103/255, 233/255),
    "R": (1, 1, 1)
}

def load_pixel_art(filename, grid_size):
    rows, cols = grid_size  # Unpack grid size

    with open(filename, "r") as file:
        lines = file.readlines()

    pixel_colors = np.zeros((rows, cols, 3), dtype=np.float32)

    row = 0  # Track valid pixel rows
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:  # Ignore comments and empty lines
            continue

        pixels = line.split(" ")
        for col, pixel in enumerate(pixels):
            if col < cols and row < rows:
                pixel_colors[row, col] = COLOR_MAP.get(pixel, (0.0, 0.0, 0.0))  # Default to black
        row += 1  # Increment row only for valid lines

    return pixel_colors

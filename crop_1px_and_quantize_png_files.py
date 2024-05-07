"""module docstring should be here"""

import os
import re

from PIL import Image
from typing import Final


def crop_image(image: Image) -> Image:
    # Get the dimensions of the image
    width, height = image.size

    # Calculate the dimensions of the cropped image
    left: Final[int] = 1
    top: Final[int] = 1
    right: Final[int] = width - 1
    bottom: Final[int] = height - 1

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image


def main():
    folder_path: Final[str] = "D:\\3phemeral/validation-docs/pix/new-20240507-TRTD"

    pattern: Final[str] = r"^\d\d (DE|EN|ES) snap-\d{6}-\d{4}.png"

    # Traverse the folder and print the names of PNG files that satisfy the pattern
    acc: int = 0
    for file_name in os.listdir(folder_path):
        if re.match(pattern, file_name):
            file_path_original: str = folder_path + '/' + file_name

            # Open the original image
            image_original = Image.open(file_path_original)
            width_original, height_original = image_original.size

            # Crop the image
            image_cropped = crop_image(image_original)
            width_cropped, height_cropped = image_cropped.size

            # Quantize the image to 256 colors
            image_quantized = image_cropped.quantize(colors=256)

            # Construct the file path for the new image by adding "-cr" before the extension
            base, ext = os.path.splitext(file_path_original)
            file_path_treated = f"{base}-TRTD{ext}"  # https://acronyms.thefreedictionary.com/trtd » Treated

            # Save the cropped image
            image_quantized.save(file_path_treated)

            acc += 1
            print(f'{acc:03d}: {file_path_original}: {width_original} x {height_original} '
                  f'» {file_path_treated}: {width_cropped} x {height_cropped}')

        # if acc > 5:
        #    break


if __name__ == '__main__':
    main()

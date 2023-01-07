from PIL import Image
from math import sqrt

ascii = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_pixel_matrix(img, width: int, height: int):
    img.thumbnail((width, height))
    pixels = list(img.getdata())
    return [pixels[i:i + img.width] for i in range(0, len(pixels), img.width)]


def pixel_to_ascii(pixel, algo: str = 'average'):
    r, g, b = pixel
    if algo == 'average':
        luminosity = (r + g + b) / 3
    elif algo == 'lightness':
        luminosity = (max(r, g, b) + min(r, g, b)) / 2
    elif algo == 'luminance':
        luminosity = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    elif algo == 'luminance_1':
        luminosity = (0.299 * r + 0.587 * g + 0.114 * b)
    elif algo == 'luminance_2':
        luminosity = sqrt(0.299 * r**2 + 0.587 * g**2 + 0.114 * b**2)
    else:
        raise NotImplementedError

    idx = int((luminosity / 255) * (len(ascii) - 1))
    return ascii[idx]


def convert_to_ascii_art(fname: str, new_image_height: int = 1000, algo: str = 'luminance'):
    img = Image.open(fname)
    print(f'Initial image size: {img.size}')
    pixels = get_pixel_matrix(img, int((new_image_height * img.width) / img.height), new_image_height)
    img_size = (len(pixels[0]), len(pixels))
    print(f'Generated image "{fname}" with size {img_size}')
    ascii_img = []
    for row in pixels:
        converted_pixels = ''
        for pixel in row:
            if '.png' in fname.lower():
                pixel = (pixel[0], pixel[1], pixel[2])
            converted_pixels += pixel_to_ascii(pixel, algo) * 2
        ascii_img.append(converted_pixels)
        print(converted_pixels)

    return ascii_img


if __name__ == '__main__':
    convert_to_ascii_art('IMG_8856.PNG', new_image_height=800, algo='luminance')

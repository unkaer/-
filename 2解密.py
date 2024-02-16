from PIL import Image
import os

def extract_rgb_from_image(image_path, block_width, block_height):
    image = Image.open(image_path)
    image_width, image_height = image.size

    rgb_colors = []

    for y in range(0, image_height, block_height):
        for x in range(0, image_width, block_width):
            center_x, center_y = x + block_width // 2, y + block_height // 2
            pixel_color = image.getpixel((center_x, center_y))
            octal_color = rgb_to_octal(pixel_color)
            rgb_colors.append(octal_color)

    return rgb_colors

def rgb_to_octal(rgb_color):
    reverse_octal_mapping = {0: '0', 36: '1', 72: '2', 108: '3', 144: '4', 180: '5', 216: '6', 252: '7'}
    octal_color = ''.join(reverse_octal_mapping[value] for value in rgb_color)
    return octal_color

def remove_padding_zeros(octal_colors):
    while octal_colors and octal_colors[-1] == '000':
        octal_colors.pop()

def concatenate_and_save_to_zip(all_rgb_colors, output_zip):
    octal_string = ''.join(octal_color for octal_color in all_rgb_colors)
    octal_string = '0o' + octal_string.rstrip('0')[:-3]
    
    decimal_number = int(octal_string, 8)
    binary_data = decimal_number.to_bytes((decimal_number.bit_length() + 7) // 8, byteorder='big')

    with open(output_zip, "wb") as file:
        file.write(binary_data)

def main():
    input_folder = 'output_images'
    block_width, block_height = 60, 60
    output_zip = 'output_data.zip'

    all_rgb_colors = []

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            rgb_colors = extract_rgb_from_image(image_path, block_width, block_height)
            all_rgb_colors.extend(rgb_colors)

    remove_padding_zeros(all_rgb_colors)
    concatenate_and_save_to_zip(all_rgb_colors, output_zip)

if __name__ == "__main__":
    main()

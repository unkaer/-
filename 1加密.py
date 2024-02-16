import zipfile
from PIL import Image
import os

def compress_to_zip(input_file, output_zip):
    # 将文件压缩为zip格式
    with zipfile.ZipFile(output_zip, 'w') as zip_file:
        zip_file.write(input_file)

def read_binary_content(file_path):
    # 使用ANSI编码二进制读取文件内容
    with open(file_path, 'rb') as file:
        return file.read()

def convert_to_octal(binary_content):
    # 获取8进制字符串内容（去除前缀 '0o'）加上 032 结尾
    octal_content = oct(int.from_bytes(binary_content, byteorder='big'))[2:] + "032"
    return octal_content

def map_octal_to_rgb(octal_content):
    # 映射表，将8进制字符映射到相应的数字
    octal_mapping = {'0': 0, '1': 36, '2': 72, '3': 108, '4': 144, '5': 180, '6': 216, '7': 252}
    
    # 将8进制字符串按照映射表转换为RGB颜色
    rgb_colors = [octal_mapping.get(char, 0) for char in octal_content]

    # 不足3的倍数的部分用0填充
    padding_length = 3 - len(rgb_colors) % 3
    rgb_colors.extend([0] * padding_length)

    # 将RGB颜色组成3个一组
    return [rgb_colors[i:i+3] for i in range(0, len(rgb_colors), 3)]

def create_image(rgb_colors, image_width, image_height, block_width, block_height, output_folder):
    # 创建图片文件夹
    os.makedirs(output_folder, exist_ok=True)

    block_index = 0
    image_index = 0

    # 遍历每个像素块
    while block_index < len(rgb_colors):
        # 创建空白图像
        image = Image.new('RGB', (image_width, image_height))

        # 遍历当前图像的每个像素块
        for y in range(0, image_height, block_height):
            for x in range(0, image_width, block_width):
                # 检查块索引是否越界
                if block_index < len(rgb_colors):
                    # 获取当前像素块对应的RGB颜色
                    current_color = tuple(rgb_colors[block_index])

                    # 填充像素块
                    for block_y in range(y, y + block_height):
                        for block_x in range(x, x + block_width):
                            image.putpixel((block_x, block_y), current_color)

                    # 更新像素块索引
                    block_index += 1

        # 更新图像索引
        image_index += 1

        # 保存生成的图像
        image_filename = f'image_{image_index:04d}.png'
        image.save(os.path.join(output_folder, image_filename))

def main():
    input_file = 'hi.txt'
    output_zip = 'output.zip'
    output_folder = 'output_images'
    image_width, image_height = 1920, 1080
    block_width, block_height = 60, 60

    # 步骤1: 将文件压缩为zip格式
    compress_to_zip(input_file, output_zip)

    # 步骤2: 读取二进制内容
    binary_content = read_binary_content(output_zip)

    # 步骤3: 转换为8进制字符串
    octal_content = convert_to_octal(binary_content)

    # 步骤4: 将8进制字符串映射到RGB颜色
    rgb_colors = map_octal_to_rgb(octal_content)

    # 步骤5: 创建图像并保存
    create_image(rgb_colors, image_width, image_height, block_width, block_height, output_folder)

if __name__ == "__main__":
    main()

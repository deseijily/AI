import os
from datetime import datetime
from PIL import Image

def rename_images_0(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 统计每个格式的图片文件的计数器
    counters = {}

    # 遍历文件列表并重命名每个图片文件
    for file_name in file_list:
        # 源文件的完整路径
        source_file_path = os.path.join(folder_path, file_name)

        # 检查文件类型并获取拍摄日期
        capture_datetime = None
        if is_image_file(file_name):
            # 图像文件，使用Pillow库获取拍摄日期
            try:
                image = Image.open(source_file_path)
                exif_data = image._getexif()
                if exif_data is None or 36867 not in exif_data:
                    continue
                capture_date = exif_data[36867]
                capture_datetime = datetime.strptime(capture_date, "%Y:%m:%d %H:%M:%S")
            except (IOError, KeyError, ValueError):
                continue
        else:
            # 非图像文件，跳过
            continue

        # 获取文件扩展名
        _, file_ext = os.path.splitext(file_name)
        file_ext = file_ext.lower()

        # 获取当前格式的图片文件的计数器
        counter = counters.get(file_ext, 1)

        # 构造新的文件名
        new_file_name = f"temp-{counter}{file_ext}"

        # 目标文件的完整路径
        target_file_path = os.path.join(folder_path, new_file_name)

        # 关闭原文件
        image.close()

        # 重命名文件
        os.rename(source_file_path, target_file_path)
        print(f"Renamed {file_name} to {new_file_name}")

        # 更新当前格式的图片文件的计数器
        counters[file_ext] = counter + 1

def rename_images_1(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 统计每个格式的图片文件的计数器
    counters = {}

    # 遍历文件列表并重命名每个图片文件
    for file_name in file_list:
        # 源文件的完整路径
        source_file_path = os.path.join(folder_path, file_name)

        # 检查文件类型并获取拍摄日期
        capture_datetime = None
        if is_image_file(file_name):
            # 图像文件，使用Pillow库获取拍摄日期
            try:
                image = Image.open(source_file_path)
                exif_data = image._getexif()
                if exif_data is None or 36867 not in exif_data:
                    continue
                capture_date = exif_data[36867]
                capture_datetime = datetime.strptime(capture_date, "%Y:%m:%d %H:%M:%S")
            except (IOError, KeyError, ValueError):
                continue
        else:
            # 非图像文件，跳过
            continue

        # 获取文件扩展名
        _, file_ext = os.path.splitext(file_name)
        file_ext = file_ext.lower()

        # 获取当前格式的图片文件的计数器
        counter = counters.get(file_ext, 1)

        # 构造新的文件名
        new_file_name = f"{capture_datetime.strftime('%Y.%#m.%#d')}-{counter}{file_ext}"

        # 目标文件的完整路径
        target_file_path = os.path.join(folder_path, new_file_name)

        # 关闭原文件
        image.close()

        # 重命名文件
        os.rename(source_file_path, target_file_path)
        print(f"Renamed {file_name} to {new_file_name}")

        # 更新当前格式的图片文件的计数器
        counters[file_ext] = counter + 1

def is_image_file(file_name):
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    _, file_ext = os.path.splitext(file_name)
    return file_ext.lower() in image_extensions

# 脚本所在文件夹路径
folder_path = os.path.dirname(os.path.abspath(__file__))

# 调用函数重命名图片文件
rename_images_0(folder_path)

# 调用函数重命名图片文件
rename_images_1(folder_path)
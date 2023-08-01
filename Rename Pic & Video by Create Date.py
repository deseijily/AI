import os
import subprocess
from datetime import datetime
from PIL import Image

# 文件类型列表
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
video_extensions = ['.mp4', '.mkv', '.avi', '.mov']

def rename_files_0(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)
    
    # 用于存储每个日期和文件扩展名组合对应的编号
    date_ext_counter = {}
    
    # 遍历文件夹中的所有文件
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        
        # 获取文件扩展名
        _, file_ext = os.path.splitext(filename)
        file_ext = file_ext.lower()
        
        capture_date = None
        # 检查文件是否为图片文件
        if file_ext in image_extensions:
            try:
                # 图像文件，使用Pillow库获取拍摄日期
                image = Image.open(file_path)
                exif_data = image._getexif()
                if exif_data is None or 36867 not in exif_data:
                    continue
                capture_date_str = exif_data[36867]
                capture_date = datetime.strptime(capture_date_str, "%Y:%m:%d %H:%M:%S").date()
                # 关闭图片文件
                image.close()
            except (IOError, KeyError, ValueError):
                continue
        elif file_ext in video_extensions:  # 检查文件是否为视频文件
            # 使用FFmpeg获取视频的拍摄日期
            command = f'ffprobe -v quiet -print_format json -show_entries stream_tags=creation_time -i "{file_path}"'
            try:
                output = subprocess.check_output(command, shell=True).decode('utf-8')
                if '"creation_time": "' in output:
                    creation_time = output.split('"creation_time": "')[1].split('.')[0]
                else:
                    print(f'No creation time found in {file_path}')
                    continue  # 移除毫秒部分
                capture_date = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S').date()
            except subprocess.CalledProcessError:
                print(f'Failed to get creation time for "{filename}"')
                continue
        
        if capture_date is None:
            continue
        
        # 根据拍摄日期创建新的文件名
        new_filename = capture_date.strftime('%y.%#m.%#d')
        
        # 检查日期和文件扩展名的组合是否已存在于计数器中，如果存在则增加编号，否则将编号初始化为1
        if (capture_date, file_ext) in date_ext_counter:
            date_ext_counter[(capture_date, file_ext)] += 1
        else:
            date_ext_counter[(capture_date, file_ext)] = 1
        
        # 添加编号到新文件名
        new_filename += f'-{date_ext_counter[(capture_date, file_ext)]}{file_ext}'
        
        # 检查文件是否与新文件名相同，如果不同则重命名文件
        if new_filename != filename:
            # 生成新文件路径
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 重命名文件
            os.rename(file_path, new_file_path)
            
            print(f'Renamed "{filename}" to "{os.path.basename(new_file_path)}"')

def rename_files_1(folder_path):
    # 获取文件夹中的所有文件
    file_list = os.listdir(folder_path)
    
    # 用于存储每个日期和文件扩展名组合对应的编号
    date_ext_counter = {}
    
    # 遍历文件夹中的所有文件
    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        
        # 获取文件扩展名
        _, file_ext = os.path.splitext(filename)
        file_ext = file_ext.lower()
        
        capture_date = None
        # 检查文件是否为图片文件
        if file_ext in image_extensions:
            try:
                # 图像文件，使用Pillow库获取拍摄日期
                image = Image.open(file_path)
                exif_data = image._getexif()
                if exif_data is None or 36867 not in exif_data:
                    continue
                capture_date_str = exif_data[36867]
                capture_date = datetime.strptime(capture_date_str, "%Y:%m:%d %H:%M:%S").date()
                # 关闭图片文件
                image.close()
            except (IOError, KeyError, ValueError):
                continue
        elif file_ext in video_extensions:  # 检查文件是否为视频文件
            # 使用FFmpeg获取视频的拍摄日期
            command = f'ffprobe -v quiet -print_format json -show_entries stream_tags=creation_time -i "{file_path}"'
            try:
                output = subprocess.check_output(command, shell=True).decode('utf-8')
                if '"creation_time": "' in output:
                    creation_time = output.split('"creation_time": "')[1].split('.')[0]
                else:
                    print(f'No creation time found in {file_path}')
                    continue  # 移除毫秒部分
                capture_date = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S').date()
            except subprocess.CalledProcessError:
                print(f'Failed to get creation time for "{filename}"')
                continue
        
        if capture_date is None:
            continue
        
        # 根据拍摄日期创建新的文件名
        new_filename = capture_date.strftime('%Y.%#m.%#d')
        
        # 检查日期和文件扩展名的组合是否已存在于计数器中，如果存在则增加编号，否则将编号初始化为1
        if (capture_date, file_ext) in date_ext_counter:
            date_ext_counter[(capture_date, file_ext)] += 1
        else:
            date_ext_counter[(capture_date, file_ext)] = 1
        
        # 添加编号到新文件名
        new_filename += f'-{date_ext_counter[(capture_date, file_ext)]}{file_ext}'
        
        # 检查文件是否与新文件名相同，如果不同则重命名文件
        if new_filename != filename:
            # 生成新文件路径
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 重命名文件
            os.rename(file_path, new_file_path)
            
            print(f'Renamed "{filename}" to "{os.path.basename(new_file_path)}"')

# 获取当前脚本所在文件夹的路径
folder_path = os.path.dirname(os.path.abspath(__file__))

# 调用函数重命名文件（避免名字被占用，先全部命名为其他名称）
rename_files_0(folder_path)

# 调用函数重命名文件
rename_files_1(folder_path)

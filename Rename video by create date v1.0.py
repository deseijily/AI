import os
import subprocess
from datetime import datetime

# 获取当前脚本所在文件夹的路径
folder_path = os.path.dirname(os.path.abspath(__file__))

# 用于存储每个日期对应的编号
date_counter = {}

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # 检查文件是否为视频文件（根据需要修改文件扩展名列表）
    if filename.lower().endswith(('.mp4', '.mkv', '.avi', 'mov')):
        # 使用FFmpeg获取视频的拍摄日期
        command = f'ffprobe -v quiet -print_format json -show_entries stream_tags=creation_time -i "{file_path}"'
        try:
            output = subprocess.check_output(command, shell=True).decode('utf-8')
            creation_time = output.split('"creation_time": "')[1].split('.')[0]  # 移除毫秒部分
            capture_date = datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S').date()
        except subprocess.CalledProcessError:
            print(f'Failed to get creation time for "{filename}"')
            continue
        
        # 根据拍摄日期创建新的文件名
        new_filename = capture_date.strftime('%Y.%#m.%#d')
        
        # 检查日期是否已存在于计数器中，如果存在则增加编号，否则将编号初始化为1
        if capture_date in date_counter:
            date_counter[capture_date] += 1
        else:
            date_counter[capture_date] = 1
        
        # 添加编号和文件格式到新文件名
        file_extension = os.path.splitext(filename)[1]  # 获取文件的扩展名
        new_filename += f'-{date_counter[capture_date]}{file_extension}'
        
        # 检查文件是否与新文件名相同，如果不同则重命名文件
        if new_filename != filename:
            # 生成新文件路径
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 重命名文件
            os.rename(file_path, new_file_path)
            
            print(f'Renamed "{filename}" to "{os.path.basename(new_file_path)}"')

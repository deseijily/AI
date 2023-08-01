import os
from docx import Document
from docx.shared import RGBColor

# 文件路径，换成你的docx文件路径
docx_path = r"替换为你的docx文件的路径 Replace with your docx file path"

# 创建Document对象
doc = Document(docx_path)

# 创建一个新的txt文件，与docx文件同名，保存在相同的文件夹内
txt_path = os.path.splitext(docx_path)[0] + '.txt'
with open(txt_path, 'w', encoding='utf-8') as f:
    # 遍历doc中的每个段落
    for para in doc.paragraphs:
        # 遍历段落中的每个运行
        for run in para.runs:
            # 检查运行的颜色是否为红色
            if run.font.color and run.font.color.rgb == RGBColor(0xFF, 0x00, 0x00):
                # 如果是红色，将文本写入txt文件，并在每个红色文本后面添加换行符
                f.write(run.text + '\n')

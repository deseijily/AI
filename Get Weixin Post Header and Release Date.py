import re
from selenium import webdriver
from bs4 import BeautifulSoup
from docx import Document
import docx.opc.constants
import docx.oxml.shared

#构造函数在Word文档的一个段落中添加一个超链接
def add_hyperlink(paragraph, url, text):
    # 获取段落的部分
    part = paragraph.part
    # 将URL添加为关系并获取其ID
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    # 创建一个XML元素用作超链接
    hyperlink = docx.oxml.shared.OxmlElement('w:hyperlink')
    # 给超链接设置r:id属性
    hyperlink.set(docx.oxml.shared.qn('r:id'), r_id)
    # 创建一个新的XML元素用作运行
    new_run = docx.oxml.shared.OxmlElement('w:r')
    # 设置运行的文本内容为传入的文本
    new_run.text = text
    # 将运行添加到超链接中
    hyperlink.append(new_run)
    # 将超链接添加到段落中
    paragraph._p.append(hyperlink)
    # 返回创建的超链接
    return hyperlink

# 从 links.txt 文件中获取需要打开的页面列表
with open('links.txt', 'r') as f:
    pages = [line.strip() for line in f.readlines()]

# 创建一个新的Chrome浏览器实例
driver = webdriver.Chrome()

# 创建一个新的 Word 文档
doc = Document()

# 循环打开每个页面
for page in pages:
    driver.get(page)  
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 提取第一行非空文字
    first_line = next(line for line in soup.text.split('\n') if line.strip())

    # 提取第一个日期
    date = re.search(r'\b\d{4}-\d{2}-\d{2}\b', soup.text)
    if date:
        date = date.group().replace('-', '')
    else:
        date = "未找到日期"

    # 在 Word 文档中添加文字和链接
    paragraph = doc.add_paragraph()
    add_hyperlink(paragraph, page, f'{date}-{first_line}')

# 保存 Word 文档
doc.save('链接命名.docx')

# 关闭浏览器
driver.quit()

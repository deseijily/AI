from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import csv
import time
from datetime import datetime

# 指定ChromeDriver的路径
driver_path = 'C:/Apps/Chrome/chromedriver.exe'  # 修改为你的chromedriver的实际路径

# 创建Service对象
s = Service(driver_path)

# 创建一个新的Chrome浏览器实例
driver = webdriver.Chrome(service=s)

# 打开登录页面
driver.get("https://i.howbuy.com/login/login.htm")  

# 执行5次Tab键操作
for _ in range(5):
    driver.switch_to.active_element.send_keys(Keys.TAB)

# 定位用户名输入框
username_input = driver.switch_to.active_element
username_input.send_keys("替换为你的账号 Replace with your ID")

# 模拟按下Tab键
username_input.send_keys(Keys.TAB)

# 定位密码输入框
password_input = driver.switch_to.active_element
password_input.send_keys("替换为你的密码 Replace with your password")

# 等待用户手动操作验证滑块
for _ in range(10):
    time.sleep(10)
    if driver.current_url == "https://i.howbuy.com/member/myhowbuy/index.htm":
        break
else:
    print("手动验证失败。")
    driver.quit()
    exit()

# 打开网页
driver.get("https://www.howbuy.com/fundtool/zixuan.htm")  # 替换为您要获取链接的网页URL

# 使用find_elements_by_tag_name方法查找网页上的所有链接元素
link_elements = driver.find_elements(By.TAG_NAME, 'a')

# 从每个链接元素提取href属性
links = [link.get_attribute('href') for link in link_elements]

# 使用正则表达式只保留“https://simu.howbuy.com/ ”开头且以“三位数字+/”结尾的链接，从而获得自选基金列表链接
links = list(filter(lambda link: link is not None and re.match(r'^https://simu\.howbuy\.com/.+\d{3}/$', link), links))

# 去重
urls = list(set(links))

# 输出链接
for url in urls:
    print(url)

data = []
for url in urls:
    # 导航到需要爬取的页面
    driver.get(url) 

    # 等待元素出现
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

    # 获取页面的HTML源代码
    html = driver.page_source

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

    # 获取第一个非空字段：基金名称
    first_nonempty_field = next(field for field in soup.stripped_strings if field)

    # 修正非空字段，只保留第一部分
    first_nonempty_field = first_nonempty_field.split(' ')[0]

    # 找到第一个"今年以来:"之前和之后的非空字段（忽略换行符）：获取今年以来收益率
    text = soup.get_text()
    pattern = r"(.*?)\s*今年以来:\s*(\S+)"
    match = re.search(pattern, text, re.DOTALL)

    # 检查是否有匹配
    if match:
        before, after = match.groups()
    else:
        # 如果没有找到"今年以来:"，那么寻找"成立以来:"
        pattern = r"(.*?)\s*成立以来:\s*(\S+)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            before, after = match.groups()
        else:
            print(f'在页面 {url} 上未找到匹配的内容')
            before, after = "", ""

    # 获取字段前后的第一个非空字段：前为截止时间，后为收益率
    before = next((s for s in reversed(before.splitlines()) if s.strip()), "")
    match = re.search(r"\[(\d{4}-\d{2}-\d{2})\]", before)
    before = match.group(1) if match else ""
    after = next((s for s in after.splitlines() if s.strip()), "")

    # 输出结果
    data.append([first_nonempty_field, before.strip(), after])

# 关闭浏览器
driver.quit()

# 获取当前日期
current_date = datetime.now().strftime("%Y%m%d")

# 保存到CSV文件，文件名包含当前日期
with open(f'output_{current_date}.csv', 'w', newline='', encoding='gbk') as f:
    writer = csv.writer(f)
    writer.writerows(data)
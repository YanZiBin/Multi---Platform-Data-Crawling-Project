import requests
from lxml import html
url="https://www.biqgg.cc/book/10439/"  # 设置目标网站URL
src=requests.get(url).content.decode('utf-8')  # 获取网页源代码
element=html.fromstring(src)  # 解析HTML
# 导入必要的库
import time
import pymongo
import re
from multiprocessing import Pool

# 连接MongoDB数据库
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["我的天赋是复活"]  # 创建数据库
collection = db["多线程"]  # 创建集合

def process_chapter(chapter_info):
    # 获取章节信息
    title = chapter_info['title']  # 获取章节标题
    full_url = chapter_info['url']  # 获取章节URL
    
    print(f"开始处理: {title}")
    
    # 添加请求头,模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    # 发送HTTP请求获取章节内容
    response = requests.get(full_url, headers=headers)
    content_text = response.content.decode('utf-8')  # 解码响应内容
    
    # 使用正则表达式提取正文内容
    content = re.findall(r'<div id="chaptercontent".*?>(.*?)请收藏本站', content_text, re.S)
    
    # 构建要存入MongoDB的数据文档
    chapter_data = {
        "标题": title,
        "内容": content,
        "链接": full_url,
    }
    
    # 将数据插入MongoDB数据库
    collection.insert_one(chapter_data)
    print(f"已保存: {title}")
    
    return True

if __name__ == '__main__':
    # 记录程序开始时间
    start_time = time.time()

    # 设置小说网站的基础URL
    base_url = "https://www.biqgg.cc"

    # 获取所有章节链接
    chapters = element.xpath('//div[@class="listmain"]/dl/dd[not(@class="more pc_none")]/a | //span[@class="dd_hide"]/dd/a')
    print(f"总共找到 {len(chapters)} 个章节，将爬取前20章")

    # 获取前20章的链接并转换为字典列表
    chapters_info = []
    for chapter in chapters[:20]:  # 只取前20章
        chapters_info.append({
            'title': chapter.text,
            'url': base_url + chapter.get('href')
        })

    print("开始爬取...")

    # 使用进程池并发执行爬虫任务,设置10个进程
    with Pool(processes=10) as pool:
        pool.map(process_chapter, chapters_info)

    # 计算程序总用时
    total_time = time.time() - start_time

    # 输出爬取结果统计信息
    print("\n全部保存完成！")
    print(f"总用时: {total_time:.2f} 秒")
    print("学号：222226205227")

from html2text import HTML2Text
from bs4 import BeautifulSoup
from lxml import etree
import requests
import os
import re


def get_article_url(html_1):   #获取分类专栏内的文章title和url
    soup=BeautifulSoup(html_1,'lxml')
    urlarray=[]
    print("该分类中的专栏文章")
    for i in soup.select('.column_article_list li'):
        title = re.sub('[\/:*?"<>|]','-',i.find('h2').text).strip()
        url=i.find('a')['href']
        print("title:",title)
        print("url:",url)
        print("----------------------------------------------------------------")
        urlarray.append(url)
    return urlarray


def remove(html): #去除文章多余内容(乱七八糟的东西“
    soup = BeautifulSoup(html, 'lxml')  # 传入解析器：lxml
    html = soup.select('article')
    return html

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    }
    # 配置header破反爬
    response = requests.get(url, headers=headers)
    # 200就继续
    if response.status_code == 200:
        html = response.content.decode("utf8")
        print("get html success!")
    else:
        print("failed!")
    return html



def crawl(html):
        tree = etree.HTML(html)
        # 找到需要的html块
        title = re.sub('[\/:*?"<>|]', '-', tree.xpath('//*[@id="articleContentId"]/text()')[0])
        print("title:", title)
        block = remove(html)
        save(block, title)
        print("finish!")
        # 完成！



def save(block, title):
    if "output" not in os.listdir():
        # 不存在输出文件夹就创建
        os.mkdir("output")
        os.mkdir("output/markdown")

    with open(f"output/markdown/{title}.md", 'w', encoding='utf8') as md_file:
        # 保存markdown

        text_maker = HTML2Text()
        # md转换
        md_text = text_maker.handle(str(block[0]))
        md_file.write(md_text)


if __name__ == '__main__':
    choice =input("输入1爬取单篇文章，输入2爬取分类专栏:")
    if choice == "1":
    #单篇文章# 你想要爬取的文章url
        url = input("输入目标url:")
        crawl(get_html(url))
    if choice == "2":
    #分类专栏# 你想要爬取的文章url
        url = input("输入目标url:")
        for url in get_article_url(get_html(url)):
            crawl(get_html(url))
    else:
        print("input error")
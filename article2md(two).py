from lxml import etree
import requests
import os
import re


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


def save(html,md):
    tree = etree.HTML(html)
    # 找到需要的html块
    title = re.sub('[\/:*?"<>|]', '-', tree.xpath('//*[@id="articleContentId"]/text()')[0])
    if "output" not in os.listdir():
        # 不存在输出文件夹就创建
        os.mkdir("output")
        os.mkdir("output/markdown")

    with open(f"output/markdown/{title}.md", 'w', encoding='utf8') as md_file:
        md_file.write(md)


if __name__ == '__main__':
    url = "https://devtool.tech/api/html-md"
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    }
    # body数据
    objurl = input("输入目标url:")
    data = {"url": objurl}
    # 发送请求
    r = requests.post(url, headers=headers, data=data)
    # 判断是否登录成功
    if r.text is not None:
        print("get markdown success!")
    else:
        print("failed!")


    html=get_html(objurl)
    md=eval(r.text)['markdown']
    save(html, md)

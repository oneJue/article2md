**爬取博客文章保存为md**

(纯净版去除多余内容，支持多平台(CSDN,简书，知乎等))

**Two Method to choose**

article2md(one).py:Method one:

article2md(two).py:Method two:

article2批量版.py：对CSDN的某一专栏下全部文章进行转化成markdown

 _________________
+ # Method one:


**思路：爬取目标html后利用html2text模块转化成markdown**
 _________________
 
## 依赖
使用pip进行安装
```
pip install html2text
pip install lxml
pip install requests
pip install beautifulsoup4
```
## 过程
爬取html
```python
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
```
去除文章多余内容，只留下正文
```python
def remove(html): #去除文章多余内容(乱七八糟的东西“
    soup = BeautifulSoup(html, 'lxml')  # 传入解析器：lxml
    html = soup.select('article')
    return html
```

创建并保存markdown文件

```python
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

```
解析标题，调用上述函数完成爬取
```python
def crawl(html):
        tree = etree.HTML(html)
        # 找到需要的html块
        title = re.sub('[\/:*?"<>|]', '-', tree.xpath('//*[@id="articleContentId"]/text()')[0])
        print("title:", title)
        block = remove(html)
        save(block, title)
        print("finish!")
        # 完成！
```

## 完整代码


```python
from html2text import HTML2Text
from bs4 import BeautifulSoup
from lxml import etree
import requests
import os
import re


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
    #单篇文章# 你想要爬取的文章url
    url = input("输入目标url:")
    crawl(get_html(url))

```
缺点：html2text模块转化成markdown会出现少量失真，需人工调整。

+ # Method two:

**思路：调用网站[HTML/URL To Markdown](https://devtool.tech/html-md)**的功能实现转化
 _________________
## 完整代码

```python

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

```
优点：语法上与原文章完全一致,保留原文所有要素，去除广告等内容
_________________

# 相关链接
[html2md批量转化版](https://github.com/oneJue/CSDN_article2md/blob/main/README.md)

# 参考资料
[【python】爬取CSDN博客文章（保存为html，txt，md）](https://blog.csdn.net/m0_53268714/article/details/121058706?spm=1001.2014.3001.5506)



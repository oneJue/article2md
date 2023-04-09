# CSDN_article2md
爬取CSDN的单篇文章或某一分类专栏下的所有文章并转化为markdowm
![image](https://github.com/oneJue/CSDN_article2md/blob/main/img/%E8%BF%90%E8%A1%8C%E6%BC%94%E7%A4%BA1.png)
![image](https://github.com/oneJue/CSDN_article2md/blob/main/img/%E8%BF%90%E8%A1%8C%E6%BC%94%E7%A4%BA2.png)
纯净版,删除评论，广告等多余内容。

# 依赖
使用pip进行安装
```
pip install html2text
pip install lxml
pip install requests
pip install beautifulsoup4
```
# 思路
爬取html
```
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

 #获取分类专栏内的文章title和url
```
def get_article_url(html_1):   #获取分类专栏内的文章title和url
    soup=BeautifulSoup(html_1,'lxml')
    urlarray=[]
    print("该分类中的专栏文章")
    for i in soup.select('.column_article_list li'):
        title = re.sub('[\/:*?"<>|]','-',i.find('h2').text).strip()
        url=i.find('a')['href']
        print("title:",title)
        print("url:",url)
        print("-------------------------------------------------")
        urlarray.append(url)
    return urlarray
```    

去除文章多余内容，只留下正文
```
def remove(html): #去除文章多余内容(乱七八糟的东西“
    soup = BeautifulSoup(html, 'lxml')  # 传入解析器：lxml
    html = soup.select('article')
    return html
```

创建并保存markdown文件

```
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
```
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

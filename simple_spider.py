# Create by MrZhang on 2019-12-06

import requests
from bs4 import BeautifulSoup
import numpy as np
import sys

sys.setrecursionlimit(10000)

class spider(object):

    def __init__(self, input_url, url_save_path, poetry_save_path):
        self.input_url = input_url
        self.url_save_path = url_save_path
        self.poetry_save_path = poetry_save_path


    def url_spider(self):
        resp = requests.get(self.input_url)
        bsobj = BeautifulSoup(resp.content, 'lxml')
        a_list = bsobj.find_all(target="_blank")
        text = ''
        print(a_list)
        for a in a_list:
            href = a.get('href')
            print(href)
            text += href+'\n'
        with open(self.url_save_path, 'w') as f:
            f.writelines(text)

    def content_spider(self, input_url):
        resp = requests.get(input_url)
        bsobj = BeautifulSoup(resp.content, 'lxml')
        poetry = {}

        selector1 = bsobj.select('div.left > div:nth-of-type(2) > div.cont > p > a')
        selector2 = bsobj.select('body > div.main3 > div.left > div:nth-of-type(2) > div.cont > div')

        title = bsobj.h1.string
        dynasty = selector1[0].string
        author = selector1[1].string
        content = selector2[-1].text.strip('\n')

        poetry['标题'] = title
        poetry['朝代'] = dynasty
        poetry['作者'] = author
        poetry['诗词'] = content

        return poetry

    def poetry_spider(self):
        poetry_list = []
        with open(self.url_save_path, 'r') as f:
            for url in f:
                poetry = self.content_spider(url.strip('\n'))
                poetry_list.append(poetry)
        poetry_array = np.array(poetry_list)
        print(poetry_array.shape)
        np.save(self.poetry_save_path, poetry_array)
        print("诗词保存完成")

    # def save_list(self, poetry_list):
    #     data_array = np.array(data_list)
    #     np.save(save_path, data_array)
    #     print("保存完成")

if __name__ == "__main__":

    input_url = 'https://www.gushiwen.org/gushi/tangshi.aspx'
    url_save_path = 'datas/poetry_url.txt'
    poetry_save_path = 'datas/poetry.npy'

    my_spider = spider(input_url, url_save_path, poetry_save_path)
    my_spider.url_spider()
    my_spider.poetry_spider()

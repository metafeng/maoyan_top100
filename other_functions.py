from mongo_main import *
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from pyecharts import options as opts
from pyecharts.charts import WordCloud as echarts_word_cloud
from pyecharts.globals import SymbolType
from efficient_apriori import apriori
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import jieba
import os
import random


def create_img():
    """
    将每部电影的海报组成成20*5的大海报
    :return: None
    """

    x = 0
    y = 0
    img_dir = 'top_100_posters/'
    images = os.listdir(img_dir)  # 返回目录下的文件列表
    random.shuffle(images)  # 将文件列表随机排序

    width = 200  # 设置单个海报的宽度
    height = int(width * 4 / 3)  # 设置单个图片的高度， 各海报比例设置为4:3
    num_line = 5  # 每行显示图片数
    out_length = int(width * num_line)  # 最终图片的宽度
    out_height = int(height * (len(images) / num_line))  # 最终图片的高度
    new_img = Image.new('RGBA', (out_length, out_height))  # 创建 长*宽 的图片用于填充各小海报

    for i in images:  # 对每一张图片逐个进行处理
        try:
            img = Image.open(img_dir + i)
        except IOError:
            print(f"第{i}张图片为空")  # 可能会出现某张图片为空的情况
        else:
            img = img.resize((width, height), Image.ANTIALIAS)  # 缩小图片
            new_img.paste(img, (x * width, y * height))  # 拼接图片，一行排满，换行拼接
            x += 1
            if x >= num_line:
                x = 0
                y += 1
    print('图片绘制完成')

    new_img.save("images/mixed_posters.png")


def count_stars(movies):
    """
    统计每位演员参演的电影及数量
    :param movies: DataFrame  电影数据
    :return: star_movies， [(star, counts)] 元组列表， 每位演员参演的电影名及数量
    """
    stars = ','.join(movies.stars)
    stars = set(stars.split(','))
    star_movies = {}
    for star in stars:
        titles = []
        for i in range(df.stars.shape[0]):
            if star in df.stars.iloc[i]:
                titles.append(df.title.iloc[i])
        star_movies[star] = len(titles), titles
    star_movies = sorted(star_movies.items(), key=lambda x: x[1][0], reverse=True)
    return star_movies


def create_word_cloud(words):
    """
    Matplotlib 绘制所有电影名词云
    :param words: 电影名
    :return: None
    """
    # 设置停用词
    stopwords = set(STOPWORDS)
    stopwords.update(['电影', '猫眼', '的'])
    cut_text = ' '.join(jieba.cut(words, cut_all=False, HMM=True))
    print(cut_text)
    wc = WordCloud(
        mask=np.array(Image.open("images/nezha.jpg")),  # 设置词云形状
        background_color='white',  # 设置背景颜色
        font_path='../fonts/msyh.ttf',  # 设置字体，针对中文的情况需要设置中文字体，否则显示乱码
        max_words=100,  # 设置字体最大值
        width=1080,  # 设置画布的宽度
        height=1900,  # 设置画布的高度
        random_state=30,  # 设置多少种随机状态，即多少种颜色
    )
    word_cloud = wc.generate(cut_text)
    # 写词云图片
    word_cloud.to_file('images/word_cloud_matplotlib.jpg')
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


def word_cloud_diamond(words) -> echarts_word_cloud:
    """
    pyecharts 绘制所有电影名词云
    :param words: [(word, counts)] 元组列表
    :return: pyecharts wordcloud 对象
    """
    c = (echarts_word_cloud().add("",
                                  words,
                                  word_size_range=[10, 50],
                                  shape=SymbolType.DIAMOND).set_global_opts(
        title_opts=opts.TitleOpts(title="猫眼电影Top100")))
    return c


def stars_relationship(stars):
    """
    探索演员之间的关系
    :param stars: 电影演员
    :return: itemsets_sort: 演员出现频率, rules： 演员之间的频繁项集
    """
    # 数据加载
    data = [names.split(",") for names in stars]
    # 挖掘频繁项集和关联规则
    itemsets, rules = apriori(data, min_support=0.015, min_confidence=1)

    itemsets_sort = {}
    for index, value in itemsets.items():
        itemsets_sort[index] = sorted(value.items(), key=lambda d: d[1], reverse=True)

    return itemsets_sort, rules


if __name__ == '__main__':
    create_img()
    # 连接MongoDB
    mongo = mongo_db('maoyan')

    # 获取所有 Top100 的电影数据
    top_100s = mongo.top_100.find()

    # 修改为DataFrame可以查看的格式
    df = pd.DataFrame(top_100s).drop("_id", axis=1)

    # 统计每位演员参演的电影及数量
    movies_of_stars = count_stars(df)
    print(movies_of_stars)

    print("绘制电影名称词云")
    create_word_cloud(''.join(df.title))
    print("pyecharts 绘制电影名词云")
    words = [(i, j) for i, j in zip(df.title[::-1], range(1, 101))]
    word_cloud_diamond(words).render("images/word_cloud_echarts.html")

    stars_relationship = stars_relationship(df.stars)
    print(f"出现频率较高的明星 \n {stars_relationship[0]}")
    print(f"频率较高的演员组合 \n {stars_relationship[1]}")



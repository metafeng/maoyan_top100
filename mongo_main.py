from top_100 import crawling_movies
from pymongo import MongoClient
import pandas as pd
import pprint
import copy

pd.set_option("display.max_columns", 100)  # 设置显示数据的最大列数，防止出现省略号…，导致数据显示不全
pd.set_option("expand_frame_repr", False)  # 当列太多时不自动换行
pd.set_option('max_colwidth', 255)  # 单元格最大数据长度


def load_config():
    import json
    with open("config.json") as config:
        return json.load(config) 


def mongo_db(db_name):
    client = MongoClient(f'{load_config()["host"]}:27017')
    mongo = client[db_name]
    return mongo


def data_to_mongo(mongo):
    mongo.top_100.drop()
    res = crawling_movies()
    res_deep_copy = copy.deepcopy(res)
    list_to_mongo = [res_deep_copy[i] for i in res_deep_copy]
    mongo.top_100.insert_many(list_to_mongo)


def top_10_upper_9(mongo, score):
    query = {"score": {"$lte": score}}
    projection = {"_id": 0}
    res = mongo.top_100.find(query, projection)
    return [i for i in res]


def after_date(mongo, date):
    query = {'release_time': {"$lt": date}}
    res = mongo.top_100.find(query)
    return [i for i in res]


def actors_movies(mongo, actor):
    query = {"stars": {"$exists": actor}}
    res = mongo.top_100_json.find(query)
    return [i for i in res]


if __name__ == "__main__":
    # 建立连接
    mongo = mongo_db('maoyan')
    # 数据入库
    # data_to_mongo(mongo)
    # 查询数据

    top_100s = mongo.top_100.find()
    pprint.pprint(top_100s)

    # 修改为DataFrame可以查看的格式
    df = pd.DataFrame(top_100s).drop("_id", axis=1)
    print(df)

    print('电影9分以上的电影有哪些 取Top10')
    pprint.pprint(top_10_upper_9(mongo, 9.0))
    print('2010年以后的电影有哪些')
    pprint.pprint(after_date(mongo, '2010-01-01'))
    print('查询张国荣的电影有哪些')
    pprint.pprint(actors_movies(mongo, '张国荣'))
    pprint.pprint([i for i in mongo.top_100.find({'1': {}})])

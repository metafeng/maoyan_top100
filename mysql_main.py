from top_100 import crawling_movies
from mysql_db import MysqlDB

mysql = MysqlDB()


def data_to_mysql():
    global mysql
    # 建库 maoyan
    sql = "create database maoyan character set utf8;"
    print(mysql.db_execute_one(sql))

    # 建表 top_100
    mysql = MysqlDB('maoyan')
    # DROP TABLE IF EXISTS `top_100`;
    sqls = """
    CREATE TABLE `top_100` (
    `id` INT ( 11 ) auto_increment NOT NULL,
    `ranking` INT ( 11 ) NOT NULL,
    `title` VARCHAR ( 255 ) NOT NULL,
    `stars` VARCHAR ( 255 ) NOT NULL,
    `release_time` VARCHAR ( 255 ) NOT NULL,
    `score` FLOAT ( 3, 1 ) NOT NULL,
    `img_url` VARCHAR ( 255 ) NOT NULL,
    PRIMARY KEY ( `id` ) USING BTREE,
    UNIQUE INDEX `title` ( `title` ) USING BTREE 
    ) ENGINE = INNODB CHARACTER 
    SET = utf8;
    """
    # sqls  = sqls.split(';')
    # for sql in sqls:
    #     print(mysql.db_execute_one(sql))
    print(mysql.db_execute_one(sqls))

    # 转换为存入数据库的数据类型
    movies_list = []
    movies_info = crawling_movies()
    for movie in movies_info.values():
        infos = [
            movie['ranking'], movie['title'], movie['stars'],
            movie['release_time'], movie['score'], movie['img_url']
        ]
        movies_list.append(tuple(infos))

    # 存入数据库
    sql = "insert into top_100 (ranking, title, stars, release_time, score, img_url) values (%s, %s, %s, %s, %s, %s);"
    print(mysql.db_insert_many(sql, movies_list))

    # 获取数据
    sql = "select * from top_100;"
    return mysql.db_query_df(sql).drop('id', axis=1)


def top_10_upper_9():
    # 电影9分以上的电影有哪些 取Top10
    sql = "SELECT * FROM `top_100` WHERE score > 9 ORDER BY score DESC limit 10;"
    return mysql.db_query_df(sql).drop('id', axis=1)


def after_date(date):
    sql = f"""
    SELECT * 
    FROM `top_100` 
    WHERE release_time > '{date}'
    ORDER BY release_time;
    """
    return mysql.db_query_df(sql).drop('id', axis=1)


def actors_movies(actor):
    sql = f"""
    SELECT * 
    FROM `maoyan`.`top_100` 
    WHERE `stars` LIKE '%{actor}%';
    """
    return mysql.db_query_df(sql).drop('id', axis=1)


if __name__ == "__main__":
    print('所有数据')
    print(data_to_mysql())
    print('电影9分以上的电影有哪些 取Top10')
    print(top_10_upper_9())
    print('2010年以后的电影有哪些')
    print(after_date('2010-01-01'))
    print('查询周星驰的电影有哪些')
    print(actors_movies('周星驰'))

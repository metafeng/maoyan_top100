import pymysql
import pandas as pd
import json


pd.set_option("display.max_columns", 100)  # 设置显示数据的最大列数，防止出现省略号…，导致数据显示不全
pd.set_option("expand_frame_repr", False)  # 当列太多时不自动换行
pd.set_option('max_colwidth', 255)  # 单元格最大数据长度


class MysqlDB(object):
    def __init__(self, db='nba'):
        self.__db = db
        
    
    def __load_config(self):
        with open("config.json") as config:
            return json.load(config) 
        
        
    def __connect(self):
        config = self.__load_config()
        return pymysql.connect(host=config["host"],
                               user=config["user"],
                               password=config["password"],
                               db=self.__db,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

    def db_query(self, sql, args=None):
        """
        sql: str, sql语句
        args（元组，列表或字典） - 与查询一起使用的参数。
        输出sql查询结果(tuple)
        """
        conn = self.__connect()
        try:
            with conn.cursor() as cursor:
                rows = cursor.execute(sql, args)  # 受影响的行数
                res = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                if rows == 0:
                    return None
                return f'Affected {rows} rows', columns, res
        except Exception as e:
            return {"error": f'Exception error: {e}'}
        finally:
            conn.close()

    def db_query_df(self, sql, args=None):
        """
        sql: sql语句
        args（元组，列表或字典） - 与查询一起使用的参数。
        查询结果输出为pandas.DataFrame
        """
        res = self.db_query(sql, args)
        if res is None:
            return None
        if type(res) == 'dict':
            return res['error']
        try:
            df = pd.DataFrame(list(res[2]), columns=res[1])
            return df
        except Exception as e:
            return {"error": f'Exception error: {e}'}

    def db_execute_one(self, sql, args=None):
        """
        执行单条sql语句
        args（元组，列表或字典） - 与查询一起使用的参数。
        """
        conn = self.__connect()
        try:
            with conn.cursor() as cursor:
                rows = cursor.execute(sql, args)
            conn.commit()
            return f'Affected {rows} rows'
        except Exception as e:
            conn.rollback()
            return {"error": f"Exception error: {e}"}
        finally:
            conn.close()

    def db_execute_many(self, sql, args=None):
        """
        执行多条sql语句
        args（元组，列表或字典） - 与查询一起使用的参数。
        """
        conn = self.__connect()
        try:
            with conn.cursor() as cursor:
                rows = cursor.executemany(sql, args)
            conn.commit()
            return f'Affected {rows} rows'
        except Exception as e:
            conn.rollback()
            return {"error": f'Exception error: {e}'}
        finally:
            conn.close()

    def db_insert_one(self, sql, args=None):
        """
        插入单条数据
        args（元组，列表或字典） - 与查询一起使用的参数。
        """
        conn = self.__connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, args)
                insert_id = cursor.lastrowid
            conn.commit()
            return insert_id
        except Exception as e:
            conn.rollback()
            return {"error": f'Exception error: {e}'}
        finally:
            conn.close()

    def db_insert_many(self, sql, args=None):
        """
        插入多条数据
        """
        conn = self.__connect()
        try:
            with conn.cursor() as cursor:
                rows = cursor.executemany(sql, args)
                insert_id = cursor.lastrowid
            conn.commit()
            return insert_id, insert_id + len(
                args) - 1, f'Affected {rows} rows'
        except Exception as e:
            conn.rollback()
            return {"error": f'Exception error: {e}'}
        finally:
            conn.close()

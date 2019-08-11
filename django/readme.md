# 猫眼Top100--Django

将前面命令行功能以web形式展示，后端框架选用DJango。

```
pip install django
```

```
django-admin startproject maoyan_top100 .
```

```
python manage.py runserver
```
在浏览器中输入[http://127.0.0.1:8000](http://127.0.0.1:8000/)访问我们的服务器，效果如下图所示。

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/Picee/image.h0d8n1qsd1r.png)

修改语言，时区

*maoyan_top100/setting.py*

```
...
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
...
```

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/Picee/image.uke1pzx9lmc.png)



```
python manage.py startapp crawler
```

项目文件树
```
(maoyan) E:\maoyan\django>tree ..  /f

│  manage.py
│
├─crawler
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations
│          __init__.py
│
└─maoyan_top100
    │  readme.md
    │  settings.py
    │  urls.py
    │  wsgi.py
    │  __init__.py
    │
    └─__pycache__
            settings.cpython-37.pyc
            urls.cpython-37.pyc
            wsgi.cpython-37.pyc
            __init__.cpython-37.pyc
```



# 数据库部分

使用Python 3需要修改**项目目录**下的`__init__.py`文件并加入如下所示的代码，这段代码的作用是将PyMySQL视为MySQLdb来使用，从而避免Django找不到连接MySQL的客户端工具而询问你：“Did you install mysqlclient? ”（你安装了mysqlclient吗？）。

*`maoyan_top100/__init__.py`*

```
import pymysql

pymysql.install_as_MySQLdb()
```

### 解决MySQL坑

- mysqlclient 版本问题
```
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
```
>解决：将  `D:\Program Files\Anaconda3\envs\maoyan\Lib\site-packages\django\db\backends\mysql\base.py` 中35,36 行注释
```
34 version = Database.version_info
35 # if version < (1, 3, 13):
36 #     raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```
-  'str' object has no attribute 'decode'

```
File "D:\Program Files\Anaconda3\envs\maoyan\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query
    query = query.decode(errors='replace')
AttributeError: 'str' object has no attribute 'decode'
```
查看 `D:\Program Files\Anaconda3\envs\maoyan\lib\site-packages\django\db\backends\mysql\operations.py`
```
    def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        query = getattr(cursor, '_executed', None)
        if query is not None:
146            query = query.decode(errors='replace')
        return query
```

> 解决：替换为下面这个版本(官网2.2.1/2.2.2(当前最新版)的包), 注意 `import force_str`

```
from django.utils.encoding import force_str

    def last_executed_query(self, cursor, sql, params):
        # With MySQLdb, cursor objects have an (undocumented) "_executed"
        # attribute where the exact query sent to the database is saved.
        # See MySQLdb/cursors.py in the source distribution.
        # MySQLdb returns string, PyMySQL bytes.
        return force_str(getattr(cursor, '_executed', None), errors='replace')
```

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/Picee/image.90ovzqh2ec.png)

## 自定义数据库

```
import json

with open("../config.json") as config:
    db_config = json.load(config)
```

```
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maoyan_admin',
        'USER': db_config["user"],
        'PASSWORD': db_config["password"],
        'HOST': db_config["host"],
        'PORT': '3306',
    },
    'crawler': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maoyan',
        'USER': db_config["user"],
        'PASSWORD': db_config["password"],
        'HOST': db_config["host"],
        'PORT': '3306',
    },
}

# 设置数据库路由规则方法
DATABASE_ROUTERS = ['maoyan_top100.database_router.DatabaseAppsRouter']

# 设置APP对应的数据库路由表
DATABASE_APPS_MAPPING = {
    # example:
    # 'app_name':'database_name',
    'crawler': 'crawler',
    'admin': 'admin'
}
```

## 从已有数据库导入 model

```
$ python .\manage.py inspectdb --database crawler > ./crawler/models.py
```

```
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Top100(models.Model):
    ranking = models.IntegerField()
    title = models.CharField(unique=True, max_length=255)
    stars = models.CharField(max_length=255)
    release_time = models.CharField(max_length=255)
    score = models.FloatField()
    img_url = models.CharField(max_length=255)

    class Meta:
        managed = True
        app_label = 'crawler'
        db_table = 'top_100'
```
添加 `app_label = 'crawler'`关联app

 >Tips：值得一提的managed=False

从输出的models.py可以看到，由inspectdb创建的model有 
**managed = False**，这意味着django不对该表进行创建、修改和删除。

managed属性默认为True，即从python manage.py migrate中创建的model，由django负责它的改动，django通过以下操作维护数据库表： 
1. migrate表记录model中类的改动变化; 

2. 执行makemigrations和migrate将改动应用到数据库表。

### 利用Django后台管理模型

1. 创建超级管理员账号。

   ```
   (maoyan) E:\maoyan\django>python manage.py createsuperuser
   用户名 (leave blank to use 'hufe'): hufe09
   电子邮件地址:
   Password:
   Password (again):
   Superuser created successfully.
   ```

2. 启动Web服务器，登录后台管理系统。

   ```
   (venv)$ python manage.py runserver
   ```

##  获取数据


```
$ python manage.py shell

>>> from crawler.models import *
>>> Top100.objects.all()
```
 ```
 <QuerySet [<Top100: Top100 object (1)>, <Top100: Top100 object (2)>, <Top100: Top100 object (3)>, <Top100: Top100 object (4)>, <Top100: Top100 object (5)>, <Top100: Top100 object (6)>,<Top100: Top100 object (7)>, <Top100: Top100 object (8)>, <Top100: Top100 object (9)>, <Top100: Top100 object (10)>, <Top100: Top100 object (11)>, <Top100: Top100 object (12)>, <Top100:Top100 object (13)>, <Top100: Top100 object (14)>, <Top100: Top100 object (15)>, <Top100: Top100 object (16)>, <Top100: Top100 object (17)>, <Top100: Top100 object (18)>, <Top100: Top100 object (19)>, <Top100: Top100 object (20)>, '...(remaining elements truncated)...']>
 ```



```
def show_movies(request):
    table_title = "猫眼Top100"
    movies_query =  Top100.objects.all()
    if movies_query:
        movies = [model_to_dict(i) for i in Top100.objects.all()]
    return render(request, 'crawler/show_movies.html',
                  {'table_title': table_title, 'movies': [i for i in movies]})
```

## 查询

```
tt = Top100.objects
# 
>>> tt.get(id=10)
<Top100: 辛德勒的名单>

# 模糊匹配
>>> tt.filter(stars__contains ="周星驰")
<QuerySet [<Top100: 唐伯虎点秋香>, <Top100: 喜剧之王>, <Top100: 大话西游之月光宝盒>, <Top100: 大话西游之大圣娶亲>]>

# 切片
>>> tt.all()[:10]
<QuerySet [<Top100: 霸王别姬>, <Top100: 肖申克的救赎>, <Top100: 罗马假日>, <Top100: 这个杀手不太冷>, <Top100: 泰坦尼克号>, <Top100: 唐伯虎点秋香>, <Top100: 魂断蓝桥>, <Top100: 乱世佳人>
, <Top100: 天空之城>, <Top100: 辛德勒的名单>]>

# 大于2010
>>> tt.filter(release_time__gt="2010")
<QuerySet [<Top100: 忠犬八公的故事>, <Top100: 疯狂原始人>, <Top100: 盗梦空间>, <Top100: 阿凡达>, <Top100: 驯龙高手>, <Top100: 速度与激情5>, <Top100: 神偷奶爸>, <Top100: 三傻大闹宝莱坞>,
 <Top100: 少年派的奇幻漂流>, <Top100: 大话西游之月光宝盒>, <Top100: 怦然心动>, <Top100: 无敌破坏王>, <Top100: 哈利·波特与死亡圣器（下）>, <Top100: 倩女幽魂>, <Top100: 蝙蝠侠：黑暗骑士
崛起>, <Top100: 甜蜜蜜>, <Top100: 初恋这件小事>, <Top100: 触不可及>, <Top100: 新龙门客栈>, <Top100: 熔炉>, '...(remaining elements truncated)...']>

# 排序
>>>tt.filter(release_time__gt="2010").order_by("-score")
<QuerySet [<Top100: 大话西游之月光宝盒>, <Top100: 疯狂原始人>, <Top100: 忠犬八公的故事>, <Top100: 教父>, <Top100: 千与千寻>, <Top100: 盗梦空间>, <Top100: 速度与激情5>, <Top100: 倩女幽魂
>, <Top100: 甜蜜蜜>, <Top100: 英雄本色>, <Top100: 三傻大闹宝莱坞>, <Top100: 少年派的奇幻漂流>, <Top100: 无敌破坏王>, <Top100: 触不可及>, <Top100: 素媛>, <Top100: 美国往事>, <Top100: 龙
猫>, <Top100: 阿凡达>, <Top100: 驯龙高手>, <Top100: 神偷奶爸>, '...(remaining elements truncated)...']>


```



## 加载静态资源
*maoyan_top100/setting.py*

```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```
```
$ python manage.py collectstatic
```

## 关闭Debug

*maoyan_top100/setting.py*

```
DEBUG = False
ALLOWED_HOSTS = ["*"]
```

## 查询

要启用`POST`请求，基于类的视图应该实现`post()`方法。但是django `ListView`类`post()`默认没有实现方法，这会引发错误。

实际上通常的做法是使用`GET`搜索选项请求。

## 结果展示

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/Picee/image.lqoou3qwb1e.png)

![image](https://raw.githubusercontent.com/hufe09/GitNote-Images/master/Picee/image.9y5zw4iti5e.png)
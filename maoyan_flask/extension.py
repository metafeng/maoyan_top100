from models import User
import json


def format_to_list(query_result):
    '''
    将从数据库查询的结果封装为列表字典
    '''
    movies_list = []
    for movie in query_result:
        movie_dict = dict(
            ranking=movie.ranking,
            title=movie.title,
            stars=movie.stars,
            release_time=movie.release_time,
            score=movie.score,
            img_url=movie.img_url,
        )
        movies_list.append(movie_dict)
    return movies_list


def list_to_json(lst):
    '''
    list 转成Json格式数据
    '''
    keys = [str(x) for x in range(len(lst))]
    list_json = dict(zip(keys, lst))
    # json转为string
    str_json = json.dumps(list_json, indent=2, ensure_ascii=False)
    return str_json


def validate(user, email, password1,  password2=None, username=None):
    
    if password2:
        if user:
            return '用户名已经存在'
        else:
            if len(username) < 4:
                return '用户名长度至少4个字符'
            elif password1 != password2:
                return '两次密码不一致'
            elif len(password1) < 6:
                return '密码长度至少6个字符'
            elif email is None:
                return '邮箱不能为空'
            else:
                return 'success'
    else:
        if user:
            if user.password == password1:
                return 'success'
            else:
                return '密码错误'
        else:
            return '用户名不存在'

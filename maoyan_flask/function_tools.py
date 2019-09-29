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

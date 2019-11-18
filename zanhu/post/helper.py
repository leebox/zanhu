from django.core.cache import cache
from .models import Post
# import redis
# from django.conf import settings
#
# pool = redis.ConnectionPool(host=settings.REDIS_HOST,
#                             port=settings.REDIS_PORT,
#                             db=settings.REDIS_DB)
# r = redis.StrictRedis(connection_pool=pool)
# # 对于大量redis连接来说，如果使用直接连接redis的方式的话，
# # 将会造成大量的TCP的重复连接，所以，就引入连接池来解决这个问题。
# # 在使用连接池连接上redis之后，可以从该连接池里面生成连接，调用完成之后，
# # 该链接将会返还给连接池，供其他连接请求调用，这样将减少大量redis连接的执行时间，
from django_redis import get_redis_connection

r = get_redis_connection("default")  # Use the name you have defined for Redis in settings.CACHES


# redis中写入对应文章的浏览次数, 并设置过期时间
def increase_page_view(post_id):
    key_flag = 'post_%d' % post_id
    view_num = cache.get(key_flag)  # 获取redis中对应文章的浏览次数
    if view_num:  # 如果缓存中有对应文章访问次数记录，则继续操作
        cache.incr(key_flag)  # 加1
        if not (view_num % 10):  # 当发现访问次数是10的倍数， 就更新数据库中文章访问次数
            Post.objects.filter(id=post_id).update(view_num=view_num)
    else:
        # 缓存中没有访问次数记录，则从数据库中获取
        view_num = Post.objects.get(id=post_id).view_num
        cache.set(key_flag, view_num + 1, None)  # none 永不过期

    return cache.get(key_flag)  # 返回最新的缓存浏览数


# 文章实时保存
def save_draft_redis(author_id, title, content):
    """
    把文章草稿存入redis哈希表
    :param content: 草稿内容
    :param title: 草稿标题
    :param author_id: 作者的PK
    :return:
    """
    # 查看是否存在此条记录
    name_flag = 'draft_%d' % author_id
    post_draft_hash = r.hgetall(name_flag)
    if post_draft_hash:
        # 如果存在，则更新
        r.hmset(name_flag, {'title': title, 'content': content})
    else:
        # 如果不存在，则创建
        r.hmset(name_flag, {'title': title, 'content': content})

    # # 遍历dict, key value 都decode
    # for k, v in r.hgetall(name_flag).items():
    #     print(k.decode('utf-8'))
    #     print(v.decode('utf-8'))
    draft = r.hgetall(name_flag)  # unicode编码的字典
    draft_utf8 = {k.decode('utf8'): v.decode('utf8') for k, v in draft.items()}
    return draft_utf8

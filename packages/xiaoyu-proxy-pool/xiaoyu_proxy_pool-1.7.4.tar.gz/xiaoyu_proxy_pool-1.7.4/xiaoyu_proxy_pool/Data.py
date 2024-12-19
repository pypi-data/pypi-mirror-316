import random

surnames = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
names = ['伟', '敏', '婷', '浩', '宇', '静', '磊', '娜', '杰', '丽']
def generate_random_str(randomlength=16):
    base_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choices(base_str, k=randomlength))
def generate_random_name():
    surname = random.choice(surnames)
    name = random.choice(names)
    return surname + name
def generate_mock_json(id):
        return {
        "code": 0,
        "msg": "0",
        "message": "0",
        "ttl": 1,
        "data": {
            "unfollow_unread": str(id).zfill(6),
            "follow_unread": generate_random_name(),
            "unfollow_push_msg": 0,
            "dustbin_push_msg": 0,
            "dustbin_unread": 0,
            "biz_msg_unfollow_unread": 0,
            "biz_msg_follow_unread": 0,
            "custom_unread": 0,
            "key1": generate_random_str(),
            "key2": generate_random_str(),
        }
    }
def nick_name_id(rand_name_id):
    if rand_name_id<1:
         print('ERROR_参数有误!')
    else:
        print('文件生成成功!')
        data = {"code": "200", "msg": "success", "data": [generate_mock_json(i+1) for i in range(rand_name_id)]}
        return data
    
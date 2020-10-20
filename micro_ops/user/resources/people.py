schema = {
    'firstname':{
            'type':'string',
            'minlength': 1,
            'maxlength':10,
        },
    'lastname':{
            'type': 'string',
            'minlength': 1,
            'maxlength': 115,
            'required': True
        },
    'role':{
        'type':'list',
        'allowed':["author","contributor","copy"],
    },
    'location':{
        'type':'dict',
        'schema':{
            'address':{'type':'string'},
            'city':{'type':'string'}
        }
    },
    'born':{
        'type':'datetime',
    },
}

people= {
    'item_title': 'people',
    # 默认情况下查找资源要同过/people/<objectid>才能找到
    # 这里添加新的只读路径，可以通过lastname来获得资源
    'additional_lookup': {
        'url':'regex("[\w]+")',
        'field':'lastname',
    },
    # 控制缓存
    'cache_control':'max-age=10,must-revalidate',
    'cache_expires': 10,
    # 覆盖全局的读写方法
    'resource_methods':['GET','POST'],
    # 设定结构
    'schema':schema,
}


    
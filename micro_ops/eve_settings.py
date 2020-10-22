import os
# import sys
# sys.path.append(os.getcwd())
from micro_ops.user.resources.people import people
from micro_ops.cmdb.schema.object import object as cmdb_object
from micro_ops.cmdb.schema.category import category

DOMAIN = {
    'people': people,
    'category': category,
    'object': cmdb_object
    }

# 这里统一规定，resource 相当于 mongo collection，item 相当于 mongo document
# 启用对资源组的增删查
# 如果忽略这一行，默认只提供查
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']


# 启用对单个资源的增删改查
# 忽略情况下只提供查
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

# We want to run seamlessly our API both locally and on Heroku
if os.environ.get('PORT'):
    # We're hosted on Heroku! Use the MongoHQ sandbox as our backend.
    MONGO_HOST = '101.132.191.123'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'root'
    MONGO_PASSWORD = 'deep2020'
    MONGO_DBNAME = 'micro_ops'
    MONGO_AUTH_SOURCE = "admin"
else:
    # Running on local machine. Let's just use the local mongod instance.

    # Please note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    MONGO_HOST = '101.132.191.123'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'root'
    MONGO_PASSWORD = 'deep2020'
    MONGO_DBNAME = 'micro_ops'
    MONGO_AUTH_SOURCE = "admin"
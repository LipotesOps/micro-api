# -*- coding: utf-8 -*-

from datetime import datetime


def genTagNum():
    fmt = "%Y%m%d%H%M%S"
    return datetime.now().strftime(fmt)


object_default_schema = {}

schema = {
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    "object_id": {
        "type": "string",
        "minlength": 1,
        "maxlength": 32,
        "regex": "^[A-Z]+$",
        "required": True,
        "unique": True,
    },
    "name": {
        "type": "string",
        "minlength": 1,
        "maxlength": 15,
        "required": True,
        # talk about hard constraints! For the purpose of the demo
        # 'lastname' is an API entry-point, so we need it to be unique.
        # 'unique': True,
    },
    # 模型描述
    "memo": {"type": "string", "maxlength": 250},
    # An embedded 'strongly-typed' dictionary.
    "category": {
        "type": "dict",
        "schema": {
            "_id": {"type": "objectid"},
            "_version": {"type": "integer"},
            "name": {"type": "string"},
        },
        "data_relation": {
            "resource": "category",
            "field": "_id",
            "embeddable": True,
            "version": True,
        },
    },
    "object_schema": {
        "type": "list",
    },
}

resource_definition = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    "item_title": "resource_definition",
    # customise url endpoint
    "url": "resource",
    # 自定义collection
    "datasource": {
        "source": "resource_definition",
    },
    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    "additional_lookup": {"url": 'regex("[\w]+")', "field": "object_id"},
    # We choose to override global cache-control directives for this resource.
    "cache_control": "max-age=10,must-revalidate",
    "cache_expires": 10,
    # most global settings can be overridden at resource level
    # 'resource_methods': ['GET', 'POST'],
    # 'item_methods': ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
    "schema": schema,
    "soft_delete": True,
}

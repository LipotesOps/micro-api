# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

import json
import copy

from flask import current_app


# on_pre_<method> and a on_pre_<method>_<resource>
def update_schema(resource, request):

    resource_definition = copy.deepcopy(DEFINITION_TEMPLATE)

    definition_data = json.loads(resource.data)
    resource_attr_list = definition_data["object_schema"]
    schema = generate_schema(resource_attr_list)

    domain_key = definition_data["object_id"]
    resource_definition["schema"] = schema

    resource_definition["item_title"] = domain_key
    resource_definition["url"] = domain_key
    resource_definition["datasource"]["source"] = "resource_{}".format(domain_key)

    current_app.register_resource(domain_key, resource_definition)
    print("object: {} is modified!".format(domain_key))


# 遍历属性列表，返回一个schema
def generate_schema(resource_attr_list):
    # 初始一个空的schema
    schema = {}
    for resource_attr in resource_attr_list:
        field_type = resource_attr["type"]
        field_map = FIELD_MAP[field_type]
        if field_type == "string":
            field_map["required"] = resource_attr["required"]
            field_map["unique"] = resource_attr["unique"]

        filed_key = resource_attr["id"]
        schema[filed_key] = field_map

    return schema


FIELD_MAP = {
    "string": {
        "type": "string",
        "minlength": 1,
        "maxlength": 15,
        "required": True,
        # talk about hard constraints! For the purpose of the demo
        # 'lastname' is an API entry-point, so we need it to be unique.
        # 'unique': True,
    },
}

SCHEMA_TEMPLATE = {
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
    # An embedded 'strongly-typed' dictionary.
    "category": {
        "type": "dict",
        "schema": {"_id": {"type": "objectid"}, "_version": {"type": "integer"}},
        "data_relation": {
            "resource": "category",
            "field": "_id",
            "embeddable": True,
            "version": True,
        },
    },
}

DEFINITION_TEMPLATE = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    "item_title": "",
    # customise url endpoint
    "url": "",
    # 自定义collection
    "datasource": {
        "source": "",
    },
    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    "additional_lookup": {"url": r'regex("[\w]+")', "field": "name"},
    # We choose to override global cache-control directives for this resource.
    "cache_control": "max-age=10,must-revalidate",
    "cache_expires": 10,
    # most global settings can be overridden at resource level
    # 'resource_methods': ['GET', 'POST'],
    # 'item_methods': ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
    "schema": SCHEMA_TEMPLATE,
    "soft_delete": True,
    "versioning": False,
}

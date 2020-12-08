# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""

import json
import copy

from flask import current_app
from eve.utils import parse_request


class EventHook(object):
    pass


# init register resource definition
# 启动时遍历已有的resource definition
def init_register():
    # app.data.init_app(app)
    app = current_app._get_current_object()
    db_client = app.data.pymongo().db
    cursor = db_client["resource_definition"].find()
    for item in cursor:
        # print(item)
        try:
            definition_data = item
            _register_once(definition_data)
        except BaseException as identifier:
            print(identifier)
        finally:
            pass
    pass


# on_pre_<method> and a on_pre_<method>_<resource>
def update_schema(resource, request):

    cursor, count = current_app.data.find("resource", parse_request("resource"), {})

    resource_definition = copy.deepcopy(DEFINITION_TEMPLATE)

    definition_data = json.loads(resource.data)
    resource_attr_list = definition_data["object_schema"]
    schema = _generate_schema(resource_attr_list)

    domain_key = definition_data["object_id"]
    resource_definition["schema"] = schema

    resource_definition["item_title"] = domain_key
    resource_definition["url"] = domain_key
    resource_definition["datasource"]["source"] = "resource_{}".format(domain_key)

    current_app.register_resource(domain_key, resource_definition)
    print("object: {} is modified and now is registered again!".format(domain_key))


# database event
# fired after a document inserted to the resource_definition collection.
def inserted_resource(items):

    definition_data = items[0]

    _register_once(definition_data)


# database event
# fired after a document updated to the resource_definition collection.
def updated_resource(updates, origin):

    origin_data = copy.deepcopy(origin)
    if len(updates.get("object_schema", [])) != 0:
        origin_data["object_schema"] = updates.get("object_schema", [])

    if len(updates.get("relation_schema", [])) != 0:
        origin_data["relation_schema"] = updates.get("relation_schema", [])

    definition_data = origin_data
    _register_once(definition_data)


# register once
def _register_once(definition_data):
    resource_attr_list = definition_data.get("object_schema", [])
    attr_schema = {}
    if len(resource_attr_list) != 0:
        attr_schema = _generate_schema(resource_attr_list)

    relation_list = definition_data.get("relation_schema", [])
    relation_schema = {}
    if len(relation_list) != 0:
        left_list = []
        for relation in relation_list:
            relation_left = relation.get("left", {})
            left_list.append(relation_left)

        relation_schema = _generate_schema(left_list)

    domain_key = definition_data["object_id"]

    resource_definition = copy.deepcopy(DEFINITION_TEMPLATE)
    merged_schema = {**attr_schema, **relation_schema}
    resource_definition["schema"] = merged_schema

    resource_definition["url"] = domain_key
    resource_definition["datasource"]["source"] = "resource_{}".format(domain_key)

    current_app.register_resource(domain_key, resource_definition)
    print("object: {} is modified and now is registered again!".format(domain_key))


# 遍历属性列表，返回一个schema
def _generate_schema(resource_attr_list):
    # 初始一个空的schema
    schema = {}
    for resource_attr in resource_attr_list:
        field_type = resource_attr["type"]
        field_map = copy.deepcopy(FIELD_MAP[field_type])
        if field_type == "string":
            field_map["required"] = resource_attr["required"]
            field_map["unique"] = resource_attr["unique"]

        filed_key = resource_attr["id"]
        schema[filed_key] = field_map

    # print(schema)
    return schema


FIELD_MAP = {
    "string": {
        "type": "string",
        "minlength": 1,
        "maxlength": 15,
        "required": False,
        # talk about hard constraints! For the purpose of the demo
        # 'lastname' is an API entry-point, so we need it to be unique.
        "unique": False,
    },
    "list": {
        "type": "list",
        "schema": {
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
    "versioning": True,
}

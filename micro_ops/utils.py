# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from flask import current_app


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


# on_pre_<method> and a on_pre_<method>_<resource>
def update_schema(resource, request):
    current_app.register_resource("music", music)
    print("object: {} is modified!".format(resource))


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

music = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    "item_title": "person",
    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    "additional_lookup": {"url": r'regex("[\w]+")', "field": "object_id"},
    # We choose to override global cache-control directives for this resource.
    "cache_control": "max-age=10,must-revalidate",
    "cache_expires": 10,
    # most global settings can be overridden at resource level
    # 'resource_methods': ['GET', 'POST'],
    # 'item_methods': ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
    "schema": schema,
}

# -*- coding: utf-8 -*-
"""pipeline models."""

from micro_ops.database import Column, PkModel, db


# 管道object
class Pipeline(PkModel):
    """A pipeline for a devops process."""

    __tablename__ = "pipeline"
    name = Column(db.String(80), nullable=False)
    app_id = Column(db.string(32))




# -*- coding: utf-8 -*-
"""User models."""

from micro_ops.database import Column, PkModel, db


class Flow(PkModel):
    """A role for a user."""

    __tablename__ = "flow"
    name = Column(db.String(80), unique=True, nullable=False)




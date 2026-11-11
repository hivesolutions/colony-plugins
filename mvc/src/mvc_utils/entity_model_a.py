#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Throwaway prototype of the async (await based) twins of the entity
model functions (get_a, find_a, count_a, load_a), bound to the models
next to the sync ones only under Python 3.7+.
"""

from . import exceptions


async def _class_get_a(
    cls,
    id_value,
    options={},
    context=None,
    namespace=None,
    entity_manager=None,
    raise_e=False,
    **kwargs
):
    entity_manager = entity_manager or cls._entity_manager
    options = cls.apply_context(
        options, context, namespace_name=namespace, entity_manager=entity_manager
    )
    entity_model = await entity_manager.get_a(cls, id_value, options, **kwargs)
    if entity_model and hasattr(entity_model, "set_request"):
        entity_model.set_request(context)
    if raise_e and not entity_model:
        raise exceptions.NotFoundError("model entity not found")
    return entity_model


async def _class_count_a(
    cls, options={}, context=None, namespace=None, entity_manager=None, **kwargs
):
    entity_manager = entity_manager or cls._entity_manager
    options = cls.apply_context(
        options, context, namespace_name=namespace, entity_manager=entity_manager
    )
    return await entity_manager.count_a(cls, options, **kwargs)


async def _class_find_a(
    cls, options={}, context=None, namespace=None, entity_manager=None, **kwargs
):
    entity_manager = entity_manager or cls._entity_manager
    options = cls.apply_context(
        options, context, namespace_name=namespace, entity_manager=entity_manager
    )
    if not cls.valid():
        return []
    entity_models = await entity_manager.find_a(cls, options, **kwargs)
    for entity_model in entity_models:
        if hasattr(entity_model, "set_request"):
            entity_model.set_request(context)
    return entity_models


async def load_a(self, *names):
    """
    Explicit (awaited) loading of the given relations, the async
    replacement of the implicit lazy loading on attribute access.
    """

    options = dict(
        eager=names,
        entities=self._entities,
        scope=self._scope,
        minimal=True,
        cache=True,
    )
    _entity = await self._entity_manager.get_a(
        self.__class__, self.get_id_value(), options
    )
    for name in names:
        setattr(self, name, getattr(_entity, name))
    return self


async def update_a(self, *args, **kwargs):
    await self._entity_manager.update_a(self, *args, **kwargs)

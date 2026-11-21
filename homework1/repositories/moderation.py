from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from errors import ItemAlreadyExistsError, ItemNotFoundError
from models.moderation import ItemModel

_COLLECTION: list[Mapping[str, Any]] = []


@dataclass(frozen=True)
class ItemStorage:
    async def create(self, **values: Any) -> Mapping[str, Any]:
        if values.get('images_qty', 0) < 0:
            raise ValueError('Количество изображений должно быть неотрицательным')

        item_id = values.get('item_id')

        if any(stored_item.get('item_id') == item_id for stored_item in _COLLECTION):
            raise ItemAlreadyExistsError

        item = dict(**values)
        _COLLECTION.append(item)

        return item

    async def get(self, item_id: int) -> Mapping[str, Any]:
        item = await self._get_item_by_id(item_id)
        return item

    async def get_many(self) -> Sequence[Mapping[str, Any]]:
        return _COLLECTION

    async def delete(self, item_id: int) -> Mapping[str, Any]:
        item = await self._get_item_by_id(item_id)

        index = _COLLECTION.index(item)
        del _COLLECTION[index]

        return item

    async def update(self, item_id: int, **changes: Any) -> Mapping[str, Any]:
        item = await self._get_item_by_id(item_id)

        for key, value in changes.items():
            item[key] = value

        return item

    async def _get_item_by_id(self, item_id: int) -> Mapping[str, Any]:
        items = [item for item in _COLLECTION if item['item_id'] == item_id]

        if not items:
            raise ItemNotFoundError()

        return items[0]


@dataclass(frozen=True)
class ItemRepository:
    item_storage: ItemStorage = ItemStorage()

    async def create(
        self,
        item_id: int,
        seller_id: int,
        is_verified_seller: bool,
        name: str,
        description: str,
        category: int,
        images_qty: int,
    ) -> ItemModel:
        raw_item = await self.item_storage.create(
            item_id=item_id,
            seller_id=seller_id,
            is_verified_seller=is_verified_seller,
            name=name,
            description=description,
            category=category,
            images_qty=images_qty,
        )
        return ItemModel(**raw_item)

    async def get(self, item_id: int) -> ItemModel:
        raw_item = await self.item_storage.get(item_id)
        return ItemModel(**raw_item)

    async def delete(self, item_id: int) -> ItemModel:
        raw_item = await self.item_storage.delete(item_id)
        return ItemModel(**raw_item)

    async def update(self, item_id: int, **changes: Any) -> ItemModel:
        raw_item = await self.item_storage.update(item_id, **changes)
        return ItemModel(**raw_item)

    async def get_many(self) -> Sequence[ItemModel]:
        return [
            ItemModel(**raw_item) for raw_item in await self.item_storage.get_many()
        ]

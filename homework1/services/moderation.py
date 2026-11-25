from dataclasses import dataclass

from repositories.moderation import ItemRepository


@dataclass(frozen=True)
class ItemService:
    item_repo: ItemRepository = ItemRepository()

    async def predict(
        self,
        item_id: int,
        seller_id: int,
        is_verified_seller: bool,
        name: str,
        description: str,
        category: int,
        images_qty: int,
    ) -> bool:

        if not (is_verified_seller or images_qty > 0):
            return False

        await self.item_repo.create(
            item_id=item_id,
            seller_id=seller_id,
            is_verified_seller=is_verified_seller,
            name=name,
            description=description,
            category=category,
            images_qty=images_qty,
        )
        return True

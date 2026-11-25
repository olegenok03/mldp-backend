from typing import Annotated

from fastapi import Depends
from services.moderation import ItemService


def item_service() -> ItemService:
    return ItemService()


ItemServiceDepend = Annotated[ItemService, Depends(item_service)]

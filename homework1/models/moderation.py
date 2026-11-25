from pydantic import BaseModel, Field


class ItemModel(BaseModel):
    item_id: int
    seller_id: int
    is_verified_seller: bool
    name: str
    description: str
    category: int
    images_qty: int = Field(ge=0)

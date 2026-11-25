from dependencies import ItemServiceDepend
from errors import ItemAlreadyExistsError
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


class CreateItemInDto(BaseModel):
    seller_id: int
    is_verified_seller: bool
    item_id: int
    name: str
    description: str
    category: int
    images_qty: int = Field(ge=0)


router = APIRouter()


@router.post('/predict', response_model=bool, status_code=status.HTTP_200_OK)
async def predict(data: CreateItemInDto, item_service: ItemServiceDepend) -> bool:
    try:
        return await item_service.predict(**data.model_dump())
    except ItemAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Объявление с таким ID уже существует',
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Внутренняя ошибка сервера',
        ) from e

class ItemAlreadyExistsError(Exception):
    """Вызывается, если объявление с таким item_id уже существует."""


class ItemNotFoundError(Exception):
    """Вызывается, если объявления с таким item_id не существует."""

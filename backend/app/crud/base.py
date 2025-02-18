from typing import Any, Dict, Generic, Sequence, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.session = session
        self.model = model

    async def get_by(
        self,
        field: str,
        value: Any,
        unique: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType] | ModelType | None:
        query = (
            select(self.model)
            .where(getattr(self.model, field) == value)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        if unique:
            return result.scalars().first()
        return result.scalars().all()

    async def create(self, attributes: Dict[str, Any]) -> ModelType:
        model = self.model(**attributes)
        self.session.add(model)
        await self.session.commit()
        return model

    async def update(self, model: ModelType, attributes: Dict[str, Any]) -> bool:
        for key, value in attributes.items():
            setattr(model, key, value)
        await self.session.commit()
        return True

    async def delete(self, model: ModelType) -> bool:
        await self.session.delete(model)
        await self.session.commit()
        return True

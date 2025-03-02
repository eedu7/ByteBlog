from typing import Any, Dict, Generic, Sequence, Type, TypeVar

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import and_, select

from app.database import Base
from app.exceptions import DatabaseException

ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    """
    A base class for performing CRUD (Create, Read, Update, Delete) operations asynchronously
    on SQLAlchemy models.
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        """
        Initializes the BaseCRUD class with the given SQLAlchemy model and session.

        Args:
            model (Type[ModelType]): The SQLAlchemy model to perform CRUD operations on.
            session (AsyncSession): The asynchronous SQLAlchemy session used to interact with the database.
        """
        self.session = session
        self.model = model

    async def get_by(
        self,
        filters: Dict[str, Any] | None = None,
        unique: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType] | ModelType | None:
        """
        Asynchronously retrieves records from the database filtered by a specific field and value.

        Args:
            filters (Dict[str, Any], Optional): A dictionary where keys are field (column) names of the model, and values are the corresponding values to match against.
            unique (bool, optional): If `True`, returns a single matching record. If `False`,
                                        a list of matching records. Defaults to `False`.
            skip (int, optional): The number of records to skip. Defaults to `0`.
            limit (int, optional): The maximum number of records to return. Defaults to `100`.

        Returns:
            Sequence[ModelType]: If `unique` is `False`, which returns a list of records or matching records.
            ModelType: If `unique` is `True`, which returns a single matching record.
            None: If no records are found matching the criteria or there is no record.

        """
        try:
            query = select(self.model)
            if filters:
                conditions = []
                for field, value in filters.items():
                    conditions.append(getattr(self.model, field) == value)
                query = query.where(and_(*conditions))
            query = query.offset(skip).limit(limit)
            result = await self.session.execute(query)
            if unique:
                return result.scalars().first()
            return result.scalars().all()

        except Exception as e:
            raise DatabaseException(f"Exception in fetching records.. {e}")

    async def create(self, attributes: Dict[str, Any]) -> ModelType:
        """
        Asynchronously creates and inserts a new record into the database.

        Args:
            attributes (Dict[str, Any]): A dictionary of attributes to set on the new model instance.

        Returns:
            ModelType: The created instance of the model

        Notes:
            The model is added to the session and committed to the database, making the record permanent.
        """
        try:
            model = self.model(**attributes)
            self.session.add(model)
            await self.session.commit()
            return model

        except Exception as e:
            raise DatabaseException(f"Exception in creating record. {e}")

    async def update(self, model: ModelType, attributes: Dict[str, Any]) -> bool:
        """
        Asynchronously updates an existing record in the database with the provided attributes.

        Args:
            model (ModelType): The model instance to be updated
            attributes (Dict[str, Any]): A dictionary of attributes and their new values to update the model.

        Returns:
            bool: `True` if the update was successul.

        Notes:
            The provided model's fields are updated with the new attributes, and changes are commited to the database.
        """
        try:
            for key, value in attributes.items():
                setattr(model, key, value)
            await self.session.commit()
            return True

        except Exception as e:
            raise DatabaseException(f"Exception in updating record. {e}")

    async def delete(self, model: ModelType) -> bool:
        """
        Asynchronously deletes a record from the database.

        Args:
            model (ModelType): The model instance to be deleted.

        Returns:
            bool: `True` if the deletion was successful.

        Notes:
            The model is removed from the session and committed, making the deletion permanent.
        """
        try:
            await self.session.delete(model)
            await self.session.commit()
            return True
        except Exception as e:
            raise DatabaseException(f"Exception in deleting record. {e}")

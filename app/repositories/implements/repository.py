from typing import TypeVar, Generic, Optional, List, Literal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from app.repositories.interfaces.i_repository import IRepository

T = TypeVar('T')
TCreate = TypeVar('TCreate')
TUpdate = TypeVar('TUpdate')

class Repository(IRepository[T, TCreate, TUpdate], Generic[T, TCreate, TUpdate]):

    def __init__(self, model_class):
        self.model_class = model_class
        self.session: Optional[Session] = None

    def set_session(self, session: Session):
        """
        Set the SQLAlchemy session for database operations.
        This method should be called before any database operations.
        """
        self.session = session


    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            order_by: Optional[str] = None,
            order_direction: Literal["asc", "desc"] = "asc"
    ) -> List[T]:
        query = self.session.query(self.model_class)

        if order_by:
            column = getattr(self.model_class, order_by)
            if order_direction == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        return query.offset(skip).limit(limit).all()

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.query(self.model_class).filter(self.model_class.id == id).first()

    def create(self, data: TCreate) -> T:
        try:
            # Convert Pydantic model to dict if needed
            if hasattr(data, 'model_dump'):  # For Pydantic v2
                item_data = data.model_dump(exclude_unset=True)
            elif hasattr(data, 'dict'):  # For Pydantic v1
                item_data = data.dict(exclude_unset=True)
            else:
                item_data = data

            # Create and add object within a transaction
            with self.session.begin():
                db_item = self.model_class(**item_data)
                self.session.add(db_item)
                # Flush to check for constraint violations before commit
                self.session.flush()
                # commit happens automatically at the end of the with block

            # Refresh outside the transaction
            self.session.refresh(db_item)
            return db_item
        except IntegrityError as e:
            # Specific error for constraint violations
            self.session.rollback()
            raise ValueError(f"Integrity error: {str(e)}")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating item: {str(e)}")

    def update(self, id: int, data: TUpdate) -> T:
        db_item = self.get_by_id(id)
        if db_item is None:
            raise ValueError(f"Item with id {id} not found")

        if hasattr(data, 'dict'):
            item_data = data.dict(exclude_unset=True)
        else:
            item_data = data
            
        for key, value in item_data.items():
            setattr(db_item, key, value)

        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def delete(self, id: int) -> None:
        db_item = self.get_by_id(id)
        if db_item is None:
            raise ValueError(f"Item with id {id} not found")

        self.session.delete(db_item)
        self.session.commit()
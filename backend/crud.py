from sqlalchemy.orm import Session
from typing import List, Type, TypeVar

import models, schemas

# Definir tipos genéricos
ModelType = TypeVar("ModelType", bound=models.Base)
SchemaType = TypeVar("SchemaType", bound=schemas.BaseModel)

def create_item(db: Session, item: SchemaType, model: Type[ModelType]) -> ModelType:
    db_item = model(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, model: Type[ModelType]) -> List[ModelType]:
    return db.query(model).all()

def get_item(db: Session, item_id: int, model: Type[ModelType]) -> ModelType:
    return db.query(model).filter(model.id == item_id).first()

def update_item(db: Session, item_id: int, item: SchemaType, model: Type[ModelType]) -> ModelType:
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int, model: Type[ModelType]) -> bool:
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

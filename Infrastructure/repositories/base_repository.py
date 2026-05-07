from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(Generic[T]):
	def __init__(self, db: Session, model: type[T]):
		self.db = db
		self.model = model
	
	# READ
	def get_by_id(self, id: int) -> Optional[T]:
		return self.db.query(self.model).filter(self.model.id == id).first()
	
	def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
		return self.db.query(self.model).offset(skip).limit(limit).all()
	
	# CREATE
	def create(self, obj: T) -> T:
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj
	
	# UPDATE
	def update(self, id: int, data: dict) -> Optional[T]:
		db_obj = self.get_by_id(id)
		if not db_obj:
			return None
		
		for key, value in data.items():
			if hasattr(db_obj, key):
				setattr(db_obj, key, value)
		
		self.db.commit()
		self.db.refresh(db_obj)
		return db_obj
	
	# DELETE
	def delete(self, id: int) -> bool:
		db_obj = self.get_by_id(id)
		if not db_obj:
			return False
		
		self.db.delete(db_obj)
		self.db.commit()
		return True
	
	# Não sei o nome CRUD que isso se aplica
	def count(self) -> int:
		return self.db.query(self.model).count()
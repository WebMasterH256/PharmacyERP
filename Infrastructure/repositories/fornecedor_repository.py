from typing			  import List, Optional, TYPE_CHECKING
from sqlalchemy.orm   import Session
from sqlalchemy		  import and_

from .base_repository import BaseRepository

if TYPE_CHECKING:
	from Domain.Compra	   import Compra
	from Domain.Fornecedor import Fornecedor
	from Domain.Lote	   import Lote


class FornecedorRepository(BaseRepository[Fornecedor]):
	def __init__(self, db:Session):
		super().__init__(db, Fornecedor)

	def get_by_nome(self, nome: str) -> List[Fornecedor]:
		return self.db.query(Fornecedor).filter(
			Fornecedor.nome.ilike(f"%{nome}%")
		).all()

	def get_by_razao_social(self, razao_social: str) -> List[Fornecedor]:
		return self.db.query(Fornecedor).filter(
			Fornecedor.razao_social.ilike(f"%{razao_social}%")
		).all()

	def get_by_cnpj(self, cnpj: str) -> Optional[Fornecedor]:
		return self.db.query(Fornecedor).filter(
			Fornecedor.cnpj == cnpj
		).first()

	def marcar_como_inativo(self, id: int) -> bool:
		fornecedor = self.get_by_id(id)
		if not fornecedor:
			return False

		fornecedor.ativo = False
		self.db.commit()
		return True
	 
	def get_lotes_of_fornecedor(self, id: int) -> List[Lote]:
		return self.db.query(Lote).filter(
			Lote.fornecedor_id == id
		).all()

	def get_compras_of_fornecedor(self, id: int) -> List[Compra]:
		return self.db.query(Compra).filter(
			Compra.fornecedor_id == id
		).all()

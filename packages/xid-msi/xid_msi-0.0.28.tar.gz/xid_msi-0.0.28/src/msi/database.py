#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from .core import IDatabase, IQuery, IRecord, ITable, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer Database.
# - cmd: msiexec /?
#--------------------------------------------------------------------------------
class Database(IDatabase):
	#--------------------------------------------------------------------------------
	# 테이블의 보유 여부.
	#--------------------------------------------------------------------------------
	def ContainsTable(self, tableName: str) -> bool:
		fieldValues: Tuple = (tableName,)
		record: IRecord = Installer.CreateRecordFromFieldValues(fieldValues)
		try:
			query: IQuery = Installer.CreateQuery(self, "SELECT Name FROM _Tables WHERE Name = ?")
			query.Execute(record)
			data = query.Fetch()
			query.Close()
			if data == None:
				return False
			elif data.GetFieldCount() == 0:
				return False
			return True
		except Exception as exception:
			return False


	#--------------------------------------------------------------------------------
	# 테이블 반환.
	#--------------------------------------------------------------------------------
	def GetTable(self, tableName: str) -> ITable:
		if not self.ContainsTable(tableName):
			return None
		
		from .table import Table
		return Table(self, tableName)


	#--------------------------------------------------------------------------------
	# 적용.
	#--------------------------------------------------------------------------------
	def Commit(self) -> None:
		rawdata = self.GetRawData()
		rawdata.Commit()


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		rawdata = self.GetRawData()
		rawdata.Close()
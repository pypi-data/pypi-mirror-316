#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import os
import traceback
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
	# 테이블 생성.
	#--------------------------------------------------------------------------------
	def CreateTable(self, tableName: str, fields: list) -> ITable:
		if not self.ContainsTable(tableName):
			fieldsString: str = str() # Component TEXT PRIMARY KEY, Directory_ TEXT, Attributes INTEGER, Guid TEXT

			fieldCount: int = builtins.len(fields)
			for index in range(fieldCount):
				field: str = fields[index]
				if not field:
					raise ValueError()
				
				values = field.split(" ")
				name: str = values[0]
				type: str = "TEXT"
				isPrimaryKey: bool = False
				wordCount: int = builtins.len(values)

				# 문제가 있음.
				if wordCount == 0:
					raise IndexError()

				if wordCount > 0:
					name: str = values[0]
				if wordCount > 1:
					type = values[1]
				if wordCount > 2:
					isPrimaryKey = True

				if index + 1 < fieldCount:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY, "
					else:
						fieldsString += f"{name} {type}, "
				else:
					if isPrimaryKey:
						fieldsString += f"{name} {type} PRIMARY KEY"
					else:
						fieldsString += f"{name} {type}"

			Installer.CreateQuery(self, f"CREATE TABLE {tableName} ({fieldsString})")
		return ITable(self, tableName)


	#--------------------------------------------------------------------------------
	# 적용.
	#--------------------------------------------------------------------------------
	def Commit(self) -> None:
		self.__database.Commit()


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		self.__database.Close()
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
import msilib # type: ignore
from .database import Database
from .query import Query
from .record import Record


#--------------------------------------------------------------------------------
# 테이블.
#--------------------------------------------------------------------------------
class Table:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: Database
	__tableName: str
	# __columnNames: list
	# __columnTypes: list

	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: Database, tableName: str) -> None:
		self.__database = database
		self.__tableName = tableName
		self.__columnNames = list()
		self.__columnTypes = list()
		# for column in self.GetColumns():
		# 	self.__columnNames.append(column[0])
		# 	self.__columnTypes.append(column[1])


	#--------------------------------------------------------------------------------
	# 컬럼 정보 반환.
	#--------------------------------------------------------------------------------
	def GetColumns(self) -> list:
		query: Query = self.__database.CreateQuery(f"SELECT Name FROM _Columns WHERE Table = {self.__tableName}")
		query.Execute()
		record: Record = query.Fetch()
		columns = list()
		while record:
			fieldName: str = record.GetFieldValueAsString(0)
			fieldTypeCode: int = record.GetFieldValueAsInteger(1)
			fieldType: str = "Other"
			if fieldTypeCode == 0:
				fieldType = "String"
			elif fieldTypeCode == 1:
				fieldType = "Integer"
			columns.append((fieldName, fieldType))
			record = query.Fetch()
		query.Close()
		return columns


	#--------------------------------------------------------------------------------
	# 모든 레코드 반환.
	#--------------------------------------------------------------------------------
	def GetAllRecords(self) -> list:
		records = list()
		view = self.__database.CreateQuery(f"SELECT * FROM {self.__tableName}")
		view.Execute(None)
		data = view.Fetch()
		while data:
			records.append(data)
			data = view.Fetch()
		view.Close()
		return records

	#--------------------------------------------------------------------------------
	# 레코드 추가.
	#--------------------------------------------------------------------------------
	def Insert(self, record: Record) -> None:
		# columnNames: str = str()
		# questionNames: str = str()
		# count: int = len(self.__columnNames)
		# for index in range(count):
		# 	columnName = self.__columnNames[index]
		# 	if index + 1 < count:
		# 		columnNames += f"{columnName}, "
		# 		questionNames += f"?, "
		# 	else:
		# 		columnNames += columnName
		# 		questionNames += f"?"

		# query = self.__database.CreateQuery(f"INSERT INTO {self.__tableName} ({columnNames}) VALUES ({questionNames})")
		# query.Execute(record)
		# query.Close()
		pass


	#--------------------------------------------------------------------------------
	# 레코드 제거.
	#--------------------------------------------------------------------------------
	def Remove(self, record: Record) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 레코드 갱신.
	#--------------------------------------------------------------------------------
	def Update(self, record: Record) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 레코드 업데이트.
	#--------------------------------------------------------------------------------
	def UpdateRecords(self, whereFieldName: str, whereFieldValue: Union[int, str, None], updateFieldName: str, updateFieldValue: Union[int, str, None])  -> None:
		record: Record = Record.CreateRecordFromFieldValues((updateFieldValue, whereFieldValue))
		view = self.__database.CreateQuery(f"UPDATE {self.__tableName} SET {updateFieldName} = ? WHERE {whereFieldName} = ?")
		view.Execute(record)
		view.Close()
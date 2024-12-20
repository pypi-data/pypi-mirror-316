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
from .query import Query
from .record import Record


#--------------------------------------------------------------------------------
# Microsoft Installer Database.
# - cmd: msiexec /?
#--------------------------------------------------------------------------------
class Database:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: msilib.Database	


	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	@property
	def Rawdata(self) -> msilib.Database:
		return self.__database


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: msilib.Database) -> None:
		self.__database = database


	#--------------------------------------------------------------------------------
	# 쿼리 생성하기. (뷰)
	#--------------------------------------------------------------------------------
	def CreateQuery(self, sqlString: str) -> Query:
		view: msilib.View = self.__database.OpenView(sqlString)
		return Query(view)


	#--------------------------------------------------------------------------------
	# 테이블의 보유 여부.
	#--------------------------------------------------------------------------------
	def ContainsTable(self, tableName: str) -> bool:
		fieldValues: Tuple = (tableName,)
		record: Record = Record.CreateRecordFromFieldValues(fieldValues)
		try:
			query: Query = self.CreateQuery("SELECT Name FROM _Tables WHERE Name = ?")
			query.Execute(record)
			data = query.Fetch()
			query.Close()
			if data == None:
				return False
			elif data.FieldCount == 0:
				return False
			return True
		except Exception as exception:
			return False


	#--------------------------------------------------------------------------------
	# 테이블 반환.
	# - 테이블의 추상화.
	#--------------------------------------------------------------------------------
	def GetTable(self, tableName: str) -> Table:
		if not self.ContainsTable(tableName):
			return None
		return Table(self, tableName)

	#--------------------------------------------------------------------------------
	# 테이블 생성.
	#--------------------------------------------------------------------------------
	def CreateTable(self, tableName: str, fields: list) -> Table:
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

			self.CreateQuery(f"CREATE TABLE {tableName} ({fieldsString})")
		return Table(self, tableName)


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


	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateDatabase(msiFilePath: str) -> Database:
		msilib.init_database(msiFilePath, msilib.schema, "undefined", "undefined", "undefined", "undefined")
		database: Database = Database.OpenDatabase(msiFilePath)
		return database


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabase(msiFilePath: str) -> Database:
		database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_TRANSACT)
		return Database(database)


	#--------------------------------------------------------------------------------
	# 불러오기. (읽기전용)
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabaseAsReadonly(msiFilePath: str) -> Database:
		database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_READONLY)
		return Database(database)


	#--------------------------------------------------------------------------------
	# GUID 생성.
	# - 생성된 값: "{12345678-1234-1234-1234-123456789ABC}"
	# - uuid4로 대체 가능.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateGUID() -> str:
		return msilib.gen_uuid()
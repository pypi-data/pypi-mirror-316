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
import msilib # type: ignore
from xpl import Interface, BaseClass, abstractmethod


#--------------------------------------------------------------------------------
# 별칭.
#--------------------------------------------------------------------------------
# NativeDatabase = msilib.Database
# NativeQuery = msilib.View
# NativeRecord = msilib.Record
# NativeOpenDatabase = msilib.OpenDatabase
# NativeGenerateUUID = msilib.gen_uuid


#--------------------------------------------------------------------------------
# 데이터베이스 인터페이스.
#--------------------------------------------------------------------------------
class IDatabase(Interface):
	@abstractmethod
	def GetRawData(self) -> msilib.Database: pass

	@abstractmethod
	def CreateQuery(self, sqlString: str) -> IQuery: pass

	@abstractmethod
	def ContainsTable(self, tableName: str) -> bool: pass

	@abstractmethod
	def GetTable(self, tableName: str) -> ITable: pass

	@abstractmethod
	def CreateTable(self, tableName: str, fields: list) -> ITable: pass

	@abstractmethod
	def Commit(self) -> None: pass

	@abstractmethod
	def Close(self) -> None: pass


#--------------------------------------------------------------------------------
# 테이블 인터페이스.
#--------------------------------------------------------------------------------
class ITable(Interface):
	def GetAllRecords(self) -> list: pass
	def Insert(self, record: IRecord) -> None: pass
	def Remove(self, record: IRecord) -> None: pass
	def Update(self, record: IRecord) -> None: pass
	def UpdateRecords(self, whereFieldName: str, whereFieldValue: Union[int, str, None], updateFieldName: str, updateFieldValue: Union[int, str, None]) -> None: pass


#--------------------------------------------------------------------------------
# 쿼리 인터페이스.
#--------------------------------------------------------------------------------
class IQuery(Interface):
	@abstractmethod
	def GetRawData(self) -> msilib.View: pass

	@abstractmethod
	def Execute(self, value: Union[IRecord, Tuple, None] = None) -> None: pass

	@abstractmethod
	def Fetch(self) -> Optional[IRecord]: pass

	@abstractmethod
	def Close(self) -> None: pass


#--------------------------------------------------------------------------------
# 레코드 인터페이스.
#--------------------------------------------------------------------------------
class IRecord(Interface):
	@abstractmethod
	def GetRawData(self) -> msilib.Record: pass

	@abstractmethod
	def GetFieldCount(self) -> int: pass

	@abstractmethod
	def GetFieldValueAsInteger(self, fieldIndex: int) -> int: pass

	@abstractmethod
	def GetFieldValueAsString(self, fieldIndex: int) -> str: pass

	@abstractmethod
	def GetFieldValue(self, fieldIndex: int) -> Union[int, str, None]: pass

	@abstractmethod
	def SetFieldValueAsInteger(self, fieldIndex: int, value: int) -> None: pass

	@abstractmethod
	def SetFieldValueAsString(self, fieldIndex: int, value: str) -> None: pass

	@abstractmethod
	def SetFieldValueAsStream(self, fieldIndex: int, filePath: str) -> None: pass

	@abstractmethod
	def SetFieldValue(self, fieldIndex: int, value: Union[int, str, None]) -> None: pass

	@abstractmethod
	def SetFieldValues(self, fieldValues: Tuple) -> None: pass


#--------------------------------------------------------------------------------
# 인스톨러.
#--------------------------------------------------------------------------------
class Installer(BaseClass):
	#--------------------------------------------------------------------------------
	# GUID 생성.
	# - 생성된 값: "{12345678-1234-1234-1234-123456789ABC}"
	# - uuid4로 대체 가능.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateGUID() -> str:
		return msilib.gen_uuid()
	

	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateDatabase(msiFilePath: str) -> IDatabase:
		msilib.init_database(msiFilePath, msilib.schema, "undefined", "undefined", "undefined", "undefined")
		database: IDatabase = Installer.OpenDatabase(msiFilePath)
		return database


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabase(msiFilePath: str) -> IDatabase:
		from .database import Database
		database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_TRANSACT)
		return Database(database)


	#--------------------------------------------------------------------------------
	# 불러오기. (읽기전용)
	#--------------------------------------------------------------------------------
	@staticmethod
	def OpenDatabaseAsReadonly(msiFilePath: str) -> IDatabase:
		from .database import Database
		database: msilib.Database = msilib.OpenDatabase(msiFilePath, msilib.MSIDBOPEN_READONLY)
		return Database(database)
	

	#--------------------------------------------------------------------------------
	# 쿼리 생성하기. (뷰)
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateQuery(database: IDatabase, sqlString: str) -> IQuery:
		from .query import Query
		view: msilib.View = database.__database.OpenView(sqlString)
		return Query(view)
	

	#--------------------------------------------------------------------------------
	# 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecord(fieldCount: int) -> IRecord:
		from .record import Record
		record: msilib.Record = msilib.CreateRecord(fieldCount)
		return Record(record)
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecordFromFieldValues(fieldValues: Tuple) -> IRecord:
		fieldCount: int = builtins.len(fieldValues)
		if fieldCount == 0:
			raise ValueError(f"invalid field values: {fieldValues}")
		
		record: IRecord = Installer.CreateRecord(fieldCount)
		record.SetFieldValues(fieldValues)
		return record
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFieldValuesFromRecord(record: IRecord) -> Optional[Tuple]:
		if not record:
			return None
		return tuple(record.GetFieldValue(index) for index in range(record.GetFieldCount()))
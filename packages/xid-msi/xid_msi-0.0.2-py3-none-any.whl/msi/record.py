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


#--------------------------------------------------------------------------------
# Microsoft Installer Database의 레코드.
#--------------------------------------------------------------------------------
class Record:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__record: msilib.Record


	#--------------------------------------------------------------------------------
	# 필드 갯수.
	#--------------------------------------------------------------------------------
	@property
	def FieldCount(self) -> int:
		return self.GetFieldCount()


	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	@property
	def Rawdata(self) -> msilib.Record:
		return self.__record


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, record: msilib.Record) -> None:
		self.__record = record

	
	#--------------------------------------------------------------------------------
	# 필드 갯수 반환.
	#--------------------------------------------------------------------------------
	def GetFieldCount(self) -> int:
		return self.__record.GetFieldCount()


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsInteger(self, fieldIndex: int) -> int:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		return self.__record.GetInteger(fieldIndex + 1)


	#--------------------------------------------------------------------------------
	# 값 반환.
	#--------------------------------------------------------------------------------
	def GetFieldValueAsString(self, fieldIndex: int) -> str:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		return self.__record.GetString(fieldIndex + 1)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def GetFieldValue(self, fieldIndex: int) -> Union[int, str, None]:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		try:
			return self.GetFieldValueAsInteger(fieldIndex)
		except Exception as exception:
			try:
				return self.GetFieldValueAsString(fieldIndex)
			except Exception as exception:
				raise


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsInteger(self, fieldIndex: int, value: int) -> None:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			self.__record.SetString(fieldIndex + 1, 0)
		elif not builtins.isinstance(value, int):
			raise ValueError(f"filePath is Not Integer.")
		self.__record.SetInteger(fieldIndex + 1, value)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsString(self, fieldIndex: int, value: str) -> None:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			self.__record.SetString(fieldIndex + 1, "")
		elif builtins.isinstance(value, str):
			self.__record.SetString(fieldIndex + 1, value)
		else:
			raise ValueError(f"{value} is Not String.")


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValueAsStream(self, fieldIndex: int, filePath: str) -> None:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif not builtins.isinstance(filePath, str):
			raise ValueError(f"not String.")
		elif not os.path.exists(filePath):
			raise FileNotFoundError(f"not exist file: {filePath}")
		self.__record.SetStream(fieldIndex + 1, filePath)


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValue(self, fieldIndex: int, value: Union[int, str, None]) -> None:
		if fieldIndex < 0 or fieldIndex >= self.FieldCount:
			raise IndexError(f"invalid field index: {fieldIndex}")
		elif value == None:
			self.SetFieldValueAsString(fieldIndex, None)
		elif builtins.isinstance(value, int):
			self.SetFieldValueAsInteger(fieldIndex, value)
		elif builtins.isinstance(value, str):
			if os.path.exists(value):
				self.SetFieldValueAsStream(fieldIndex, value)
			else:
				self.SetFieldValueAsString(fieldIndex, value)
		else:
			raise ValueError(f"connot be a field value: {value}")


	#--------------------------------------------------------------------------------
	# 값 설정.
	#--------------------------------------------------------------------------------
	def SetFieldValues(self, fieldValues: Tuple) -> None:
		fieldIndex: int = 0
		for fieldValue in fieldValues:
			self.SetFieldValue(fieldIndex, fieldValue)
			fieldIndex += 1


	#--------------------------------------------------------------------------------
	# 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecord(fieldCount: int) -> Record:
		record: msilib.Record = msilib.CreateRecord(fieldCount)
		return Record(record)
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateRecordFromFieldValues(fieldValues: Tuple) -> Record:
		fieldCount: int = builtins.len(fieldValues)
		if fieldCount == 0:
			raise ValueError(f"invalid field values: {fieldValues}")
		
		record: Record = Record.CreateRecord(fieldCount)
		record.SetFieldValues(fieldValues)
		return record
	

	#--------------------------------------------------------------------------------
	# 필드값 목록으로부터 레코드 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFieldValuesFromRecord(record: Record) -> Optional[Tuple]:
		if not record:
			return None
		return tuple(record.GetFieldValue(index) for index in range(record.FieldCount))
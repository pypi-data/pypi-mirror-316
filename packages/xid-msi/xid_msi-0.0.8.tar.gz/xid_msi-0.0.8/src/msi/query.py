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
from .core import IQuery, IRecord, Installer


#--------------------------------------------------------------------------------
# Microsoft Installer Database의 SQL 처리자. (View)
#--------------------------------------------------------------------------------
class Query(IQuery):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__view: msilib.View


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, view: msilib.View) -> None:
		self.__view = view


	#--------------------------------------------------------------------------------
	# 래핑한 원래 객체.
	#--------------------------------------------------------------------------------
	def GetRawData(self) -> msilib.View:
		self.__view


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def Execute(self, value: Union[IRecord, Tuple, None] = None) -> None:
		if value == None:
			self.__view.Execute(None)
		elif builtins.isinstance(value, IRecord):
			self.__view.Execute(value.Rawdata)
		elif builtins.isinstance(value, Tuple):
			record: IRecord = Installer.CreateRecordFromFieldValues(value)
			self.__view.Execute(record.Rawdata)
		else:
			raise ValueError(f"invalid value: {value}")


	#--------------------------------------------------------------------------------
	# 가져오기.
	#--------------------------------------------------------------------------------
	def Fetch(self) -> Optional[IRecord]:
		record = self.__view.Fetch()
		if not record:
			return None

		from .record import Record
		return Record(record)


	#--------------------------------------------------------------------------------
	# 닫기.
	#--------------------------------------------------------------------------------
	def Close(self) -> None:
		self.__view.Close()
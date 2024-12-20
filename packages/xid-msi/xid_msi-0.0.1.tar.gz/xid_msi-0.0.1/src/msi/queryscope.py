#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import traceback
from .database import Database
from .query import Query


#--------------------------------------------------------------------------------
# Microsoft Installer View Creator With Context Manager.
#--------------------------------------------------------------------------------
class QueryScope:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__database: Database
	__view: Query
	__sqlString: str

	
	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self, database: Database, sqlString: str) -> None:
		self.__database = database
		self.__view = None
		self.__sqlString = sqlString


	#--------------------------------------------------------------------------------
	# With 시작됨.
	#--------------------------------------------------------------------------------
	def __enter__(self) -> Query:
		self.__view = self.__database.CreateQuery(self.__sqlString)
		return self.__view


	#--------------------------------------------------------------------------------
	# With 종료됨.
	#--------------------------------------------------------------------------------
	def __exit__(self, exceptionType : Optional[type], exceptionValue: Optional[BaseException],
			  tracebackException: Optional[traceback.TracebackException]) -> bool:
		if self.__view:
			self.__view.Close()
			return True
		if tracebackException:
			traceback.print_tb(tracebackException)  
		return False
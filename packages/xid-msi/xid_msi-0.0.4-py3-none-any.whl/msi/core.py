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
from xpl import Interface


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
	pass


#--------------------------------------------------------------------------------
# 테이블 인터페이스.
#--------------------------------------------------------------------------------
class ITable(Interface):
	pass


#--------------------------------------------------------------------------------
# 쿼리 인터페이스.
#--------------------------------------------------------------------------------
class IQuery(Interface):
	pass


#--------------------------------------------------------------------------------
# 레코드 인터페이스.
#--------------------------------------------------------------------------------
class IRecord(Interface):
	pass
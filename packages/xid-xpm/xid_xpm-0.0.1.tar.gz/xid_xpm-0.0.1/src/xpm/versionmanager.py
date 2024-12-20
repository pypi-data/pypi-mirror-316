#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
from xpl import Builtins
from .versiondata import VersionData


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
UTF8: str = "utf-8"
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"


#--------------------------------------------------------------------------------
# 버전 매니저.
#--------------------------------------------------------------------------------
class VersionManager:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__versionData: VersionData


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.__versionData = VersionData()


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	def CreateVersionToFile(versionFilePath: str) -> None:
		with builtins.open(versionFilePath, mode = FILE_WRITETEXT, encoding = UTF8) as file:
			file.write()
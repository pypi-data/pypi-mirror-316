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
import sys
import unittest
from xpl import Builtins, Path



#--------------------------------------------------------------------------------
# 테스트 매니저. (유닛테스트 기반)
#--------------------------------------------------------------------------------
class TestManager:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	value: str


	#--------------------------------------------------------------------------------
	# 생성됨.
	#--------------------------------------------------------------------------------
	def __init__(self) -> None:
		self.value = "VALUE!!"


	#--------------------------------------------------------------------------------
	# 실행.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Run() -> None:
		Builtins.Print(f"[TestManager] TestManager.Run()")

		rootPath: str = Path.GetRootPath(__file__)
		sourcePath: str = os.path.join(rootPath, "src")
		testPath: str = os.path.join(rootPath, "test")

		# 루트 경로 추가.
		# 루트의 자식인 src와 test를 메인 패키지로 추가하기 위한 설정.
		if rootPath not in sys.path:
			sys.path.append(rootPath)
			Builtins.print("[TestManager] Add Project Root Path: {rootPath}")

		# 소스 경로 추가.
		# src 안의 서브패키지들을 메인 패키지 처럼 src. 접근 없이 곧바로 사용하기 위한 설정.
		if sourcePath not in sys.path:
			sys.path.append(sourcePath)
			Builtins.print("[TestManager] Add Source Packages Path: {sourcePath}")

		# 테스트 로더 생성.
		loader = unittest.TestLoader()

		# test 폴더 내의 test_ 로 시작하는 모든 스크립트 파일을 기준으로 테스트 스위트 생성.
		suite = loader.discover(start_dir = "test", pattern = "test_*.py")

		# 테스트 실행기 생성.
		runner = unittest.TextTestRunner()
		runner.run(suite)


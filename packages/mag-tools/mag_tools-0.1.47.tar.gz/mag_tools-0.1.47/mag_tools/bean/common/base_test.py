from typing import Optional

from mag_tools.model.common.log_type import LogType

from mag_tools.log.logger import Logger
from model.test.test_component_type import TestComponentType


class BaseTest:
    def __init__(self, name:str, index:Optional[int]=None, test_component_type:Optional[TestComponentType] = None, description:Optional[str]=None):
        self._name = name
        self._index = index
        self._test_component_type = test_component_type
        self._description = description

    def start(self, driver):
        self._report()
        return driver

    def _report(self):
        Logger.info(LogType.FRAME, f"开始执行{self._test_component_type.desc}({self._name})")

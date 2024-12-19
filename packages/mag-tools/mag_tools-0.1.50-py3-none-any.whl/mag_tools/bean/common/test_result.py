from typing import Optional


class TestResult:
    def __init__(self, success:Optional[bool]=True, message:Optional[str]=None):
        self.success = success
        self.message = message

    def __str__(self):
        return '测试成功' if self.success else f'测试失败：{self.message}'
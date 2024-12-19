class BaseTest:
    def __init__(self, name, index=None, description=None):
        self._name = name
        self._index = index
        self._description = description

    def start(self, driver):
        self._report()
        return driver

    def _report(self):
        raise NotImplementedError("This method should be overridden in subclasses")

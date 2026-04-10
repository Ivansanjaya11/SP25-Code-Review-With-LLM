from unittest.mock import MagicMock

class MockDummy(MagicMock):
    def __getattr__(self, name):
        return MagicMock()
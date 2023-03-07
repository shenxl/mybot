from unittest import mock

def create_mock_firestore():
    # 初始化 mock 的 Firebase Admin SDK
    app_mock = mock.MagicMock()
    db_mock = mock.MagicMock()
    app_mock.options.return_value = {}
    db_mock.collection.return_value = db_mock
    db_mock.document.return_value = db_mock
    db_mock.set.return_value = None
    return app_mock, db_mock

class MockFirebase:
    app_mock, db_mock = create_mock_firestore()

    @classmethod
    def cleanup(cls):
        cls.app_mock.reset_mock()
        cls.db_mock.reset_mock()
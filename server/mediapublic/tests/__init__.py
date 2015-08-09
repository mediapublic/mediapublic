import unittest
import transaction

from pyramid import testing

from mediapublic.models import DBSession


class TestStatusSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from mediapublic.models import (
            Base,
            Users,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Users(first='Joe', last='Test')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_passing_view(self):
        from mediapublic.views import get_status
        request = testing.DummyRequest()
        info = get_status(request)
        self.assertEqual(info['web'], True)

from .base import BaseTestCase

class TestHelloWorld(BaseTestCase):
    def test_hello_world(self):
        def hello_world():
            from . import hello_world
        self.assertStdout('Hello, World!', hello_world)
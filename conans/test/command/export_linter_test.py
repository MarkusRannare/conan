import unittest
from conans.paths import CONANFILE
from conans.test.utils.tools import TestClient
import six


class ExportLinterTest(unittest.TestCase):

    def test_basic(self):
        client = TestClient()
        conanfile = """
from conans import ConanFile
class TestConan(ConanFile):
    name = "Hello"
    version = "1.2"
    def build(self):
        print("HEllo world")
        for k, v in {}.iteritems():
            pass
"""
        client.save({CONANFILE: conanfile})
        client.run("export lasote/stable")
        if six.PY2:
            self.assertIn("ERROR: Py3 incompatibility. Line 7: print statement used",
                          client.user_io.out)
            self.assertIn("ERROR: Py3 incompatibility. Line 8: Calling a dict.iter*() method",
                          client.user_io.out)

        self.assertIn("WARN: Linter. Line 8: Unused variable 'k'",
                      client.user_io.out)
        self.assertIn("WARN: Linter. Line 8: Unused variable 'v'",
                      client.user_io.out)

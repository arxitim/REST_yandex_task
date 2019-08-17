from django.test import TestCase


class PostTest(TestCase):
    def test_wrong_condition(self):
        self.assertEqual(True, True)
        self.assertEqual(True, False)

    def test_wrong_format(self):
        self.assertEqual(False, True)
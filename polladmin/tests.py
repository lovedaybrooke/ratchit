from django.test import TestCase

from models import *

class ModelsTestCase(TestCase):
    fixtures = ['models.json']

    def test_unique_title_for_polls(self):
        """ Test that new event cannot use the same title as existing """

        self.assertFalse(
            Poll.unique_title("Drinks"),
            "Duplicate event title not detected by Event.unique_title()")
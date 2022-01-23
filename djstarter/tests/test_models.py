from django.test import TestCase

from djstarter.models import ListItem


class ListItemTests(TestCase):

    """
    List Item Model Tests
    """

    @classmethod
    def setUpTestData(cls):
        cls.group = 'group_1'
        cls.label = 'label_1'
        cls.value = 'value_1'

    def test_list_item_str(self):
        list_item = ListItem(group=self.group, label=self.label, value=self.value)
        self.assertEquals(str(list_item), f'ListItem: {self.label} / {self.value}')

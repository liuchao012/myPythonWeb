from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from listsss.models import Item, List
from listsss.views import home_page
import unittest
from django.core.exceptions import ValidationError

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_liat = List.objects.first()
        self.assertEqual(saved_liat, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_save_item = saved_items[0]
        second_save_item = saved_items[1]
        self.assertEqual(first_save_item.text, 'The first (ever) list item')
        self.assertEqual(first_save_item.list, list_)
        self.assertEqual(second_save_item.text, 'Item the second')
        self.assertEqual(second_save_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_=List.objects.create()
        item = Item(list= list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/list/%d/'%(list_.id,))

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from listsss.models import Item
from listsss.views import home_page
import unittest


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        print("第x个测试通过了")
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        resp = home_page(request)

        # 使用render_to_string ,django自带函数 生成string字符串，和渲染获取到的字符串对比
        #### 注释：这个没有办法解决，两次生成得tocken值是不相同的，所以先注释掉这个字段对应的断言
        expected_html = render_to_string('listsss/home.html', request=request)

        # .decode()将字符串转换成unicode
        # self.assertEqual(resp.content.decode(), expected_html)

        self.assertTrue(resp.content.startswith(b'<html>'))
        self.assertIn(b"<title>To-Do lists</title>", resp.content)
        self.assertTrue(resp.content.endswith(b'</html>'))

    def test_home_page_can_save_a_POST_request(self):
        requ = HttpRequest()
        requ.method = 'POST'
        requ.POST['item_text'] = 'A new list item'

        rep = home_page(requ)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        # 下面这部分单独拿出去做一个 单独的单元测试
        # self.assertIn('A new list item', rep.content.decode())
        # post 请求后页面重定向
        # self.assertEqual(rep.status_code, 302)
        # self.assertEqual(rep['location'], '/')

    def test_home_page_redirects_after_POST(self):
        requ = HttpRequest()
        requ.method = 'POST'
        requ.POST['item_text'] = 'A new list item'

        rep = home_page(requ)
        self.assertEqual(rep.status_code, 302)
        self.assertEqual(rep['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        req = HttpRequest()
        rep = home_page(req)

        self.assertIn('itemey 1', rep.content.decode())
        self.assertIn('itemey 2', rep.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_save_item = saved_items[0]
        second_save_item = saved_items[1]
        self.assertEqual(first_save_item.text, 'The first (ever) list item')
        self.assertEqual(second_save_item.text, 'Item the second')

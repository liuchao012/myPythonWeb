from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from listsss.models import Item, List
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

    # def test_home_page_only_saves_items_when_necessary(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

    # 中途这个用例不要了
    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #
    #     req = HttpRequest()
    #     rep = home_page(req)
    #
    #     self.assertIn('itemey 1', rep.content.decode())
    #     self.assertIn('itemey 2', rep.content.decode())


# class ItemModelTest(TestCase):
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


class ListViewTest(TestCase):
    def test_home_page_displays_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        resp = self.client.get('/list/the-only-list-in-the-world/')

        self.assertContains(resp, 'itemey 1')
        self.assertContains(resp, 'itemey 2')

    def test_uses_list_template(self):
        resp = self.client.get('/list/the-only-list-in-the-world/')
        self.assertTemplateUsed(resp, 'listsss/list.html')


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post('/list/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        # requ = HttpRequest()
        # requ.method = 'POST'
        # requ.POST['item_text'] = 'A new list item'
        #
        # rep = home_page(requ)
        #
        # self.assertEqual(Item.objects.count(), 1)
        # new_item = Item.objects.first()
        # self.assertEqual(new_item.text, 'A new list item')
        #
        # # 下面这部分单独拿出去做一个 单独的单元测试
        # # self.assertIn('A new list item', rep.content.decode())
        # # post 请求后页面重定向
        # # self.assertEqual(rep.status_code, 302)
        # # self.assertEqual(rep['location'], '/')

    def test_redirects_after_POST(self):
        rep = self.client.post('/list/new', data={'item_text': 'A new list item'})
        self.assertEqual(rep.status_code, 302)

        # django 的检查项
        self.assertRedirects(rep, '/list/the-only-list-in-the-world/')

        # requ = HttpRequest()
        # requ.method = 'POST'
        # requ.POST['item_text'] = 'A new list item'
        #
        # rep = home_page(requ)
        # self.assertEqual(rep.status_code, 302)
        # self.assertEqual(rep['location'], '/list/the-only-list-in-the-world/')

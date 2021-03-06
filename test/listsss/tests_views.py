from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape
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

        # self.assertTrue(resp.content.startswith(b'<html>'))
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


class ListViewTest(TestCase):
    # def test_home_page_displays_all_list_items(self):
    def test_home_page_displays_only_items_for_that_list(self):
        # list_ = List.objects.create()
        # Item.objects.create(text='itemey 1', list=list_)
        # Item.objects.create(text='itemey 2', list=list_)

        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other itemey 1', list=other_list)
        Item.objects.create(text='other itemey 2', list=other_list)

        # resp = self.client.get('/list/the-only-list-in-the-world/')
        resp = self.client.get('/list/%d/' % (correct_list.id,))

        self.assertContains(resp, 'itemey 1')
        self.assertContains(resp, 'itemey 2')
        self.assertNotContains(resp, 'other itemey 1')
        self.assertNotContains(resp, 'other itemey 2')

    def test_uses_list_template(self):
        # resp = self.client.get('/list/the-only-list-in-the-world/')
        list_ = List.objects.create()
        resp = self.client.get('/list/%d/' % (list_.id,))
        self.assertTemplateUsed(resp, 'listsss/list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        resp = self.client.get('/list/%d/' % (correct_list.id,))
        self.assertEqual(resp.context['list'], correct_list)

    def test_can_save_a_POST_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/list/%d/' % (correct_list.id,),
                         data={'item_text': 'A new item for an existiong list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existiong list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        resp = self.client.post('/list/%d/' % (correct_list.id,),
                                data={'item_text': 'A new item for an existiong list'})
        self.assertRedirects(resp, '/list/%d/' % (correct_list.id,))

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        resp = self.client.post('/list/%d/'%(list_.id,), data={"item_text":''})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'listsss/list.html')
        ex_error=escape('You cant have an empty list item')
        self.assertContains(resp, ex_error)

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
        # self.assertEqual(rep.status_code, 302)

        new_list = List.objects.first()
        self.assertRedirects(rep, '/list/%d/' % (new_list.id,))
        # django 的检查项
        # self.assertRedirects(rep, '/list/the-only-list-in-the-world/')
        # 这段重新修改

        # requ = HttpRequest()
        # requ.method = 'POST'
        # requ.POST['item_text'] = 'A new list item'
        #
        # rep = home_page(requ)
        # self.assertEqual(rep.status_code, 302)
        # self.assertEqual(rep['location'], '/list/the-only-list-in-the-world/')

    def test_validation_error_are_sent_back_to_home_page_template(self):
        resp = self.client.post('/list/new', data={'item_text': ''})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'listsss/home.html')
        ex_error = escape("You cant have an empty list item")
        print(resp.content.decode())
        self.assertContains(resp, ex_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/list/new', data={"item_text": ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


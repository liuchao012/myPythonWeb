from django.shortcuts import render, redirect  # redirect是python的重定向方法
from django.http import HttpResponse
from listsss.models import Item, List


# Create your views here.
def home_page(request):
    # return HttpResponse("<html><title>To-Do lists</title></html>")
    # if (request.method=='POST'):
    #    return HttpResponse(request.POST['item_text'])

    # 新加了页面这里就可以删除了
    # if (request.method == 'POST'):
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/list/the-only-list-in-the-world/')

    ##第二种方法
    # else:
    #     new_item_text = ''
    # return render(request, 'listsss/home.html', {'new_item_text':new_item_text})

    ##第一种方法
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    # return render(request, 'listsss/home.html', {'new_item_text':request.POST.get('item_text','')})

    # 这里首页不用展示相关的数据了
    # items_list = Item.objects.all()
    # return render(request, 'listsss/home.html', {'items_list': items_list})
    return render(request, 'listsss/home.html')


def view_list(request):
    items_list = Item.objects.all()
    return render(request, 'listsss/list.html', {'items_list': items_list})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/list/the-only-list-in-the-world/')


class home_page_class():
    pass

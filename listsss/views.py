from django.shortcuts import render, redirect  # redirect是python的重定向方法
from django.http import HttpResponse
from listsss.models import Item, List
from django.core.exceptions import ValidationError


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


def view_list(request, list_id):
    error = None
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            #简化
            #return redirect('/list/%d/' % (list_.id,))
            return redirect(list_)
        except ValidationError:
            item.delete()  # 不知道为什么要加这一步，书里面没有这步骤，书上说抓取到这个错误就不会存到数据库里面了，可还是存进去了
            error = 'You cant have an empty list item'
    return render(request, 'listsss/list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        item.delete()  # 不知道为什么要加这一步，书里面没有这步骤，书上说抓取到这个错误就不会存到数据库里面了，可还是存进去了
        error = 'You cant have an empty list item'
        return render(request, 'listsss/home.html', {"error": error})
    # 重新定义到有效地址
    # return redirect('/list/the-only-list-in-the-world/')
    # 去除硬编码
    # return redirect('/list/%d/' % (list_.id,))
    return redirect('view_list', list_.id)


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/list/%d/' % (list_.id,))


class home_page_class():
    pass



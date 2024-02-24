from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator    
from django.utils import timezone

from .form import ContactPostForm, MemoPostForm, FinancialPostForm
from .models import Contact, Memo, Diary, FinancialRecord

from itertools import groupby
from operator import attrgetter



# Create your views here.
# 通讯录信息
def contact_list(request):

    id = request.user.id
    search = request.GET.get('search')
    if search:
        all = Contact.objects.filter(
            Q(name__icontains=search))
    else:
        search = ''
        all = Contact.objects.all()

    contact_info = []    

    for contact in all:
        if contact.creater.id == id:
            contact_info.append(contact)

    paginator = Paginator(contact_info, 4)
    page = request.GET.get('page')
    contact_info = paginator.get_page(page)

    contacts = {'contact_info': contact_info,
                'search': search,}
    return render(request,'private_info/contact.html', contacts)

# 检查登录
@login_required(login_url='/userprofile/login/')
def contact_create(request):
    if request.method == 'POST':
        post_form = ContactPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post_form = post_form.save(commit=False)
            print(request.user.id)
            new_post_form.creater =  User.objects.get(id=request.user.id)
            new_post_form.save()
            return redirect('private_info:contact_list')
        else:
            return HttpResponse('喜报:post error!')
    else:
        post_form = ContactPostForm()
        contacts = {'post_form': post_form}
        return render(request, 'private_info/create.html', contacts)
    

@login_required(login_url='/userprofile/login/')
def contact_detail(request, id):
    contact = get_object_or_404(Contact, id=id)
    
    print(request.method,'q')

    context = {
        'contact': contact}
    return render(request, 'private_info/detail.html', context)



@login_required(login_url='/userprofile/login/')
def contact_updata(request, id):
    # 获取通讯录id
    contact = Contact.objects.get(id=id)
    print(request.method)
    if request.method == 'POST':
        if request.user != contact.creater:
            return HttpResponse('喜报:你不是创建者')
        post_form = ContactPostForm(request.POST, request.FILES)

        print(post_form.data)
        # 获取创建者id
        post_form.creater = User.objects.get(id=request.user.id)
        if post_form.is_valid():
            
            contact.name = request.POST['name']
            contact.contact_info = request.POST['contact_info'] 
            contact.work_place = request.POST['work_place']
            contact.city = request.POST['city']
            contact.notes = request.POST['notes']
            if request.FILES.get('avatar'):
                contact.avatar = request.FILES.get('avatar')
            contact.save()
            return redirect('private_info:detail', id = id)
        else:
            return HttpResponse('喜报:提交表单不合法')

@login_required(login_url='/userprofile/login/')
def contact_delete(request, id):
    if request.method == 'POST':
        contact = Contact.objects.get(id=id)

        if request.user.id != contact.creater.id:
            return HttpResponse("喜报:你不能删它！")
        contact.delete()
        return redirect('private_info:contact_list')
    else:
        return HttpResponse('喜报:不允许POST以外的请求')
    
# 备忘录
def memo_list(request):

    id = request.user.id
    search = request.GET.get('search')
    if search:
        all = Memo.objects.filter(
            Q(event__icontains=search)|
            Q(location__icontains=search)
            ).order_by('created')
    else:
        search = ''
        all = Memo.objects.all()

    memo_info = []    

    for memo in all:
        if memo.creater.id == id:
            memo_info.append(memo)

    paginator = Paginator(memo_info, 4)
    page = request.GET.get('page')
    memo_info = paginator.get_page(page)

    contacts = {'contact_info': memo_info,
                'search': search,}
    return render(request,'private_info/memo.html', contacts)

# 检查登录
@login_required(login_url='/userprofile/login/')
def memo_create(request):
    if request.method == 'POST':
        post_form = MemoPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            new_post_form = post_form.save(commit=False)
            print(request.user.id)
            new_post_form.creater =  User.objects.get(id=request.user.id)
            new_post_form.save()
            return redirect('private_info:memo_list')
        else:
            return HttpResponse('喜报:post error!')
    else:
        post_form = MemoPostForm()
        contacts = {'post_form': post_form}
        return render(request, 'private_info/memo_create.html', contacts)
    
@login_required(login_url='/userprofile/login/')
def memo_detail(request, id):
    contact = get_object_or_404(Memo, id=id)
    
    print(request.method,'q')

    context = {
        'contact': contact}
    return render(request, 'private_info/memo_detail.html', context)

@login_required(login_url='/userprofile/login/')
def memo_updata(request, id):
    # 获取通讯录id
    memo = Memo.objects.get(id=id)
    print(request.method)
    if request.method == 'POST':
        if request.user != memo.creater:
            return HttpResponse('喜报:你不是创建者')
        post_form = MemoPostForm(request.POST)

        print(post_form.data)
        # 获取创建者id
        post_form.creater = User.objects.get(id=request.user.id)
        if post_form.is_valid():
            memo.time = request.POST['time']
            memo.location = request.POST['location']
            memo.event = request.POST['event']
            memo.save()
            return redirect('private_info:memo_detail', id = id)
        else:
            return HttpResponse('喜报:提交表单不合法')
    
@login_required(login_url='/userprofile/login/')
def memo_delete(request, id):
    if request.method == 'POST':
        memo = Memo.objects.get(id=id)

        if request.user.id != memo.creater.id:
            return HttpResponse("喜报:你不能删它！")
        memo.delete()
        return redirect('private_info:memo_list')
    else:
        return HttpResponse('喜报:不允许POST以外的请求')
    
# financial
def financial_list(request):
    id = request.user.id
    search = request.GET.get('search')
    if search:
        all = FinancialRecord.objects.filter(
            Q(expense_time__icontains=search)|
            Q(expense_item__icontains=search)
            ).order_by('-expense_time')
    else:
        search = ''
        all = FinancialRecord.objects.all().order_by('-expense_time')

    financial_info = []    

    for financial in all:
        if financial.creater.id == id:
            financial_info.append(financial)

    paginator = Paginator(financial_info, 4)
    page = request.GET.get('page')
    financial_info = paginator.get_page(page)

    # 将表单按时间进行group by
    grouped_records = []
    for key, group_financial in groupby(financial_info, key=lambda x: x.expense_time.date()):
        print(group_financial)
        grouped_records.append({
            'date': key,
            'records': list(group_financial)})

    for records in grouped_records:
        income = 0
        expense = 0
        for record in records['records']:
            income += record.total_income
            expense += record.expense_amount
        records['income'] = income
        records['expense'] = expense

    contexts = {'contact_info': grouped_records,
                'search': search,}
    return render(request,'private_info/financial.html', contexts)

@login_required(login_url='/userprofile/login/')
def financial_create(request):
    if request.method == 'POST':
        post_form = FinancialPostForm(request.POST)
        if post_form.is_valid():
            new_post_form = post_form.save(commit=False)
            print(request.user.id)
            new_post_form.creater =  User.objects.get(id=request.user.id)
            new_post_form.save()
            return redirect('private_info:financial_list')
        else:
            return HttpResponse('喜报:post error!')
    else:
        post_form = FinancialPostForm()
        current_time = timezone.now().strftime('%Y-%m-%dT%H:%M')  # 获取当前时区时间并格式化
        contacts = {'post_form': post_form,
                    'current_time': current_time}
        return render(request, 'private_info/financial_create.html', contacts)
    
@login_required(login_url='/userprofile/login/')
def financial_detail(request, id):
    contact = get_object_or_404(FinancialRecord, id=id)

    context = {
        'contact': contact}
    return render(request, 'private_info/financial_detail.html', context)

@login_required(login_url='/userprofile/login/')
def financial_updata(request, id):
    # 获取通讯录id
    financial = FinancialRecord.objects.get(id=id)
    print(request.method)
    if request.method == 'POST':
        if request.user != financial.creater:
            return HttpResponse('喜报:你不是创建者')
        post_form = FinancialPostForm(request.POST)


        # 获取创建者id
        post_form.creater = User.objects.get(id=request.user.id)
        if post_form.is_valid():
            financial.total_income = request.POST['total_income']
            financial.expense_time = request.POST['expense_time']
            financial.expense_item = request.POST['expense_item']
            financial.expense_amount = request.POST['expense_amount']
            financial.save()
            return redirect('private_info:financial_detail', id = id)
        else:
            return HttpResponse('喜报:提交表单不合法')
    
    
@login_required(login_url='/userprofile/login/')
def financial_delete(request, id):
    if request.method == 'POST':
        contact = FinancialRecord.objects.get(id=id)

        if request.user.id != contact.creater.id:
            return HttpResponse("喜报:你不能删它！")
        contact.delete()
        return redirect('private_info:financial_list')
    else:
        return HttpResponse('喜报:不允许POST以外的请求')
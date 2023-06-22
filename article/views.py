from bleach import clean
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views import View
from matplotlib.pyplot import title
from article.form import ArticlePostForm

from article.models import ArticleColumn, ArticlePost
from comment.models import Comment
# 引入分页模块
from django.core.paginator import Paginator                                                                                                                                                                          
from django.contrib.auth.decorators import login_required
# 引入 Q 对象
from django.db.models import Q
# 引入评论表单
from comment.forms import CommentForm

import markdown

# Create your views here.


def article_list(request):
    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    order = request.GET.get('order')
    search = request.GET.get('search')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    paginator = Paginator(article_list,3)
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    context = {
        'articles':articles, 
        'order':order,
        'search': search,
        'column': column,
        'tag': tag,
        }
    return render(request,'article/list.html',context)

def article_detail(request, id):
    
    # 取出文章的作者
    article = get_object_or_404(ArticlePost,id=id)
    # 编辑模板
    # 将markdown语法渲染成html样式
    # article.body = markdown.markdown(article.body,
    #     extensions=[
    #     # 包含 缩写、表格等常用扩展
    #     # 'markdown.extensions.extra',
    #     # 语法高亮扩展
    #     'markdown.extensions.codehilite',
    #     ])
    md = markdown.Markdown(
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        # 目录扩展
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)
    if article.column != None:
        columns = ArticleColumn.objects.get(title=article.column)
    else:
        columns = None
    # 引入评论表单
    comment_form = CommentForm()
    # 取出文章评论 
    comments = Comment.objects.filter(article=id)
    
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    
    context = {'article':article, 
                'toc':md.toc, 
                'comments': comments,
                'columns':columns,
                'comment_form':comment_form,
                }
    return render(request,'article/detail.html', context)

# 检查登录
@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
         # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据,但暂不提交到数据库中
            new_article = article_post_form.save(commit=False)
             # 指定目前登录的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            # 栏目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
     # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文
        context = { 'article_post_form': article_post_form, 'columns':columns }
        # 返回模板
        return render(request, 'article/create.html', context)
    
# 删文章
# def article_delete(request, id):
#     # 根据 id 获取需要删除的文章
#     article = ArticlePost.objects.get(id=id)
#     # 调用.delete()方法删除文章
#     article.delete()
#     # 完成删除后返回文章列表
#     return redirect("article:article_list")

# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse("仅允许post请求")

# 文章更新
@login_required(login_url='/userprofile/login/')
def article_updata(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单,更新titile、body字段
    GET方法进入初始表单页面
    id: 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    
    if request.method == 'POST':
        # 过滤非作者的用户
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        # 将提交的数据赋值到表单实例中
        # 指定目前登录的用户为作者
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 指定目前登录的用户为作者
        article_post_form.author = User.objects.get(id=request.user.id)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存

            article.title = request.POST['title']
            article.body = request.POST['body']
            # 栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                 article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            # redirect通过url路径响应对应的视图函数 而render加载一个模板 
            return redirect('article:article_detail', id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例(未绑定)
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        columns = ArticleColumn.objects.all()
        context = {
            'article':article,
            'article_post_form':article_post_form,
            'columns':columns,
            'tags':','.join([x for x in article.tags.names()])
        }
        return render(request,'article/updata.html',context)

#点赞
class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
        





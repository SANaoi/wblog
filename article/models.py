from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from matplotlib.pyplot import title
# Django-taggit
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.

class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ArticlePost(models.Model):
    # 发布者
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 文章标题
    title = models.CharField(max_length =100)
    # 文章正文
    body = models.TextField()
    #  创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更改时间
    updated = models.DateTimeField(auto_now=True)
    # 浏览量
    total_views = models.PositiveIntegerField(default=0)
    # 文章栏目的 “一对多” 外键
    column = models.ForeignKey(
        ArticleColumn,
        null = True,
        blank= True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    # 文章标题图
    avatar = models.ImageField(upload_to='article/%Y%m%d/',blank=True)
    # 文章标签 '多对多关系'
    tags = TaggableManager(blank=True)
    
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
    	# '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
    def __str__(self) -> str:
        # return self.title 将文章标题返回
        return self.title
    
    # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 保存时处理图像
    def save(self,*args,**kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)
        # 固定宽度缩放图片大小
        if self.avatar and not kwargs.get('updata_fields'):
            image = Image.open(self.avatar)
            (x,y) = image.size
            new_x = 400
            new_y = int(new_x*(y/x))
            resized_image = image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article
        
    def was_created_recently(self):
        diff = timezone.now() - self.created
        
        # if diff.days <= 0 and diff.seconds < 60:
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False
    



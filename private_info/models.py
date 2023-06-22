from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    creater = models.ForeignKey(
        User,
        null = True, 
        on_delete=models.CASCADE,
        related_name='creater')
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    work_place = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    notes = models.TextField()
    # 联系人头像
    avatar = models.ImageField(upload_to='private_info/%Y%m%d/', blank=True)

    def __str__(self):
        return self.name

# 备忘录
class Memo(models.Model):
    creater = models.ForeignKey(
        User,
        null = True, 
        on_delete=models.CASCADE,
        related_name='creater_memo')
    # 设定提醒时间
    time = models.DateTimeField(blank=True, null = True, )
    event = models.TextField()
    location = models.CharField(max_length=100)
    #  创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更改时间
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event
    
    @property
    def default_datetime(self):
        return self.time.strftime("%Y-%m-%dT%H:%M")

# 日记
class Diary(models.Model):
    creater = models.ForeignKey(
        User,
        null = True, 
        on_delete=models.CASCADE,
        related_name='creater_diary')
    location = models.CharField(max_length=100)
    event = models.TextField()
    person = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)
    # 更改时间
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.event
        

# 个人财物管理
class FinancialRecord(models.Model):
    creater = models.ForeignKey(
        User,
        null = True, 
        on_delete=models.CASCADE,
        related_name='creater_financial')
    # 收入
    total_income = models.DecimalField(max_digits=10, decimal_places=2)
    # 条款
    expense_item = models.CharField(max_length=100)
    # 开支
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    # 时间 默认创建时间
    expense_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.expense_item
    
    @property
    def default_datetime(self):
        return self.expense_time.strftime("%Y-%m-%dT%H:%M")
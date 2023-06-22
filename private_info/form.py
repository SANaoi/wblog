# 引入表单类
from django import forms
# 引入文章模型
from .models import Contact, Memo, Diary, FinancialRecord

class ContactPostForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'contact_info','work_place',
                  'city', 'notes', 'avatar')
        
class MemoPostForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ('event', 'time', 'location')

class FinancialPostForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ('expense_item','expense_time' ,'total_income','expense_amount')
from django.contrib import admin
from .models import Contact, Memo, Diary, FinancialRecord
# Register your models here.
admin.site.register(Contact)
admin.site.register(Memo)
admin.site.register(Diary)
admin.site.register(FinancialRecord)

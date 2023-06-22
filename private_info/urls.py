from django.urls import path
from . import views

app_name = 'private_info'

urlpatterns = [
    path('contact_list/', views.contact_list, name='contact_list'),
    path('create/', views.contact_create, name='create'),
    path('detail/<int:id>',views.contact_detail, name='detail'),
    path('updata/<int:id>',views.contact_updata, name='updata'),
    path('delete/<int:id>',views.contact_delete, name='delete'),
    # memo
    path('memo_list/', views.memo_list, name='memo_list'),
    path('memo_create/', views.memo_create, name='memo_create'),
    path('memo_detail/<int:id>', views.memo_detail, name='memo_detail'),
    path('memo_updata/<int:id>', views.memo_updata, name='memo_updata'),
    path('memo_delete/<int:id>', views.memo_delete, name='memo_delete'),
    # Financial
    path('financial_list/', views.financial_list, name='financial_list'),
    path('financial_create/', views.financial_create, name='financial_create'),
    path('financial_detail/<int:id>',views.financial_detail, name='financial_detail'),
    path('financial_updata/<int:id>',views.financial_updata, name='financial_updata'),
    path('financial_delete/<int:id>', views.financial_delete, name='financial_delete'),
    ]
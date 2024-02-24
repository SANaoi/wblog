"""wblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# 新引入的模块
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls
<<<<<<< HEAD
from userprofile.views import cover
=======
>>>>>>> 4f4ef326541ee198e31d7224c9f28195571e27e5

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls', namespace='article')),
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('password-reset', include('password_reset.urls')),
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
    # notice
    path('notice/',include('notice.urls', namespace='notice')),
<<<<<<< HEAD
    # 私人信息
    path('private_info/', include('private_info.urls', namespace='private_info')),
    # 首页
    path('',cover)
=======
>>>>>>> 4f4ef326541ee198e31d7224c9f28195571e27e5
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

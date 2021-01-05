

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views
from drf_matchweb.settings import MEDIA_ROOT
from django.conf.urls import url,include
from django.views.static import serve


urlpatterns = [
    path('api/',include("user.urls") ),
    path('api/',include("app.match.urls") ),
    # 富文本编辑
    url(r'ueditor/', include('DjangoUeditor.urls')),

    # jwt的认证接口
    url(r'^api/login/', obtain_jwt_token),

    url(r"^media/(?P<path>.*)$", serve, {"document_root": MEDIA_ROOT}),
]

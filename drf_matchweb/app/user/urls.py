from . import views
from django.urls import path

# 管理员对用户操作
adminuser_urls = views.AdminToUserViewset.as_view()

admin_detailuser_urls = views.AdminDetailUserViewset.as_view()

#用户逻辑
user_urls = views.UserViewset.as_view()

# 学院专业
major_urls = views.MajorViewset.as_view()

urlpatterns = [
    # 用户逻辑
    path("user/", user_urls),

    # 管理员对用户操作
    path("admin/user/<int:id>/",admin_detailuser_urls),
    path("admin/user/",adminuser_urls),

    # 获取专业学院
    path("major/",major_urls),


]

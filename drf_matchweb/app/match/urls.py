from . import views
from django.urls import path

# 老师管理比赛
teachermatch_detail_urls = views.TeacherMatchViewset.as_view({
        "delete":"destory",
        "get":"retrieve",
})

teachermatch_urls = views.TeacherMatchViewset.as_view({
        "post":"create",
        "get":"list",
        "put":"update",
})

# 老师管理流程
teacherprocess_detail_urls = views.MatchPorocess.as_view({
        "delete":"destory",
        "get":"retrieve",
})
teacherprocess_urls = views.MatchPorocess.as_view({
        "post":"create",
        "put":"update",
})

# 种类
type_urls = views.TypeViewset.as_view({
        "get":"list",
        "post": "create",

})
typedetail_urls = views.TypeViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',

})

# 评论
comment_urls = views.CommentViewset.as_view({
    'post': 'create',
    "get":"list"
})
commentdetail_urls = views.CommentViewset.as_view({
    "get":"retrieve",
})

# 普通用户报名管理
user_match_urls = views.SignMatchViewset.as_view()

# 管理员管理比赛
adminmatch_urls = views.AdminMatchViewset.as_view()

# 管理员管理报名
adminusermatch_urls = views.AdminSignViewset.as_view()


# 管理员管理评论
admincomment_urls = views.AdminCommentViewset.as_view({
    'get': 'list',
})

# 管理员管理评论
admincomment_detail_urls = views.AdminCommentViewset.as_view({
    'delete': 'destroy',
})

# 老师管理新闻
news_urls = views.NewsViewset.as_view({
        "get":"list",
        "post": "create",

})
newsdetail_urls = views.NewsViewset.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',

})

# 管理员管理比赛结果
admin_matchresult_urls = views.TeacherMatchResultViewset.as_view()

# 按种类看比赛
typematchs_urls = views.TeacherMatchViewset.as_view({"get":"list"})
typematchs_detail_urls = views.TeacherMatchViewset.as_view({"get":"retrieve"})

# 查询比赛
match_find_urls = views.FindViewset.as_view()

urlpatterns = [
    path("teacher/match/",teachermatch_urls),
    path("teacher/match/<int:pk>/",teachermatch_detail_urls),
    path("teacher/process/",teacherprocess_urls),
    path("teacher/process/<int:pk>",teachermatch_detail_urls),
    path("type/<int:pk>",typedetail_urls),
    path("type/",type_urls),
    path("usermatch/",user_match_urls),

    path("admin/match/",adminmatch_urls),
    path("admin/usermatch/",adminusermatch_urls),

    path("comment/",comment_urls),
    path("comment/<int:match_id>/",commentdetail_urls),
    path("admin/comment/<int:pk>/",admincomment_detail_urls),
    path("admin/comment/",admincomment_urls),

    path("news/",news_urls),
    path("news/<int:pk>/",newsdetail_urls),

    path("teacher/result/",admin_matchresult_urls),

    path("matchtype/",typematchs_urls),
    path("matchtype/<int:pk>/", typematchs_detail_urls),

    path("find/",match_find_urls)
]

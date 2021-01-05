import datetime

from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .seriailzers import CreateMatchSerializer,MatchProceessSerializer,DetailMatchSerializer,TypeSerializer,UpdataMatchSerializer,UserandMatchSerializer,CommentSerializer,NewsSerializer,TypeMatchSerializer
from .models import Match,Process,Type,UseAndMatch,Comment,News
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from app.user.models import UserProfile
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from app.utils.permissions import AdminPermission,UserPermission,TeacherPermission
# Create your views here.

class P1(PageNumberPagination):
    """
    基于页码
    """
    # 默认每页显示的数据条数
    page_size = 10
    # 获取url参数中设置的每页显示数据条数
    page_size_query_param = 'pagesize'
    # 获取url中传入的页码key
    page_query_param = 'page'
    # 最大支持的每页显示的数据条数
    max_page_size = 50


########### 管理员
class AdminMatchViewset(APIView):
    """管理员对比赛操作"""
    permission_classes = (IsAuthenticated, AdminPermission)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    def put(self,request,*args,**kwargs):
        # 对比赛审核
        check = request.data.get("check",None)
        match_id = request.data.get("match",None)


        if not all([check,match_id]):
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数不完整",
                             }, status=status.HTTP_200_OK)

        if int(check) not in [1,2]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数错误",
                             }, status=status.HTTP_200_OK)

        try:
            match = Match.objects.get(id=match_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到比赛",
                             }, status=status.HTTP_200_OK)

        match.check = check
        match.save()
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        # 按比赛审核状态返回比赛 不提交返回全部 0：返回没审核 1审核通过 2审核未通过
        check = request.GET.get("check",None)


        p1 = P1()

        if check is None:
            matchs = Match.objects.all().order_by("sign_starttime")
        else:
            matchs = Match.objects.filter(check=check).all().order_by("sign_starttime")

        page_list = p1.paginate_queryset(queryset=matchs, request=request, view=self)

        serializer = DetailMatchSerializer(instance=page_list, many=True)
        return Response({"status_code": status.HTTP_200_OK,
                            "message": "ok",
                            "results": {"data":serializer.data,"count":len(matchs)},
                        }, status=status.HTTP_200_OK)


class AdminSignViewset(APIView):
    """管理员对报名信息操作"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    def put(self,request,*args,**kwargs):
        # 对报名信息审核
        check = request.data.get("check", None)
        group_id = request.data.get("group", None)

        if not all([check, group_id]):
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数不完整",
                             }, status=status.HTTP_200_OK)

        if int(check) not in [1, 2]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数错误",
                             }, status=status.HTTP_200_OK)

        try:
            leader_gropu = UseAndMatch.objects.get(id=group_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到比赛",
                             }, status=status.HTTP_200_OK)

        leader_gropu.check = check
        leader_gropu.save()

        # 团队其他人状态都变成审核通过
        for username in leader_gropu.group.split(","):
            UseAndMatch.objects.filter(user=UserProfile.objects.get(username=username),match=leader_gropu.match).update(check=check)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        # 按队伍审核状态返回比赛
        check = request.GET.get("check", None) # 不提交check返回所有状态
        match_id = request.GET.get("match",0) # 不提交match，返回所有match


        p1 = P1()
        if match_id != 0:
            try:
                match = Match.objects.get(id=match_id)
            except Exception as e:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "找不到该比赛",
                                 "results": [],
                                 }, status=status.HTTP_200_OK)
            if check is None:
                useandmatch = UseAndMatch.objects.filter(is_leader=1, match=match).all().order_by("signtime")

            else:
                useandmatch = UseAndMatch.objects.filter(is_leader=1, match=match, check=check).all().order_by("signtime")


        else:
            if check is None:
                useandmatch = UseAndMatch.objects.filter(is_leader=1).all().order_by("signtime")

            else:
                useandmatch = UseAndMatch.objects.filter(is_leader=1, check=check).all().order_by("signtime")

        page_list = p1.paginate_queryset(queryset=useandmatch, request=request, view=self)


        serializer = UserandMatchSerializer(instance=page_list, many=True)
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": {"data":serializer.data,"count":len(useandmatch)},
                         }, status=status.HTTP_200_OK)


class AdminCommentViewset(viewsets.GenericViewSet,mixins.ListModelMixin):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    queryset = Comment.objects.filter().all().order_by("-starttime")
    pagination_class = P1
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk",0)

        try:
            comment = Comment.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "没有该评论",
                         }, status=status.HTTP_200_OK)

        comment.delete()
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)









###########老师逻辑

class TeacherMatchViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """比赛逻辑"""
    serializer_class = DetailMatchSerializer
    pagination_class = P1
    queryset = Match.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def create(self,request,*args,**kwargs):
        """创建比赛"""
        data = request.data

        serializer = CreateMatchSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        if data["classes"] == 0:
            Match.objects.create(title=data["title"],count=data["count"],content=data["content"],sign_starttime=data["sign_starttime"],
                                 sign_endtime=data["sign_endtime"],type=Type.objects.get(id=data["type"]),classes=0,check=0)
        else:
            Match.objects.create(title=data["title"], count=data["count"], content=data["content"],
                                 sign_starttime=data["sign_starttime"],
                                 sign_endtime=data["sign_endtime"], type=Type.objects.get(id=data["type"]),group_maxcount=data["group_maxcount"],group_mincount=data["group_mincount"],classes=1,check=0)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def destory(self,request,*args,**kwargs):
        """删除比赛"""
        id = kwargs.get("pk",0)

        try:
            match = Match.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "找不到该比赛",
                         }, status=status.HTTP_200_OK)
        match.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self,request,*args,**kwargs):
        p1 = P1()

        page_list = p1.paginate_queryset(queryset=Match.objects.filter().all().order_by("sign_starttime"), request=request, view=self)

        serializer = DetailMatchSerializer(instance=page_list, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = UpdataMatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        count = Match.objects.filter(title=request.data.get("title")).exclude(id=request.data.get("pk")).count()

        if count > 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "比赛不能同名",
                             }, status=status.HTTP_200_OK)
        try:
            match = Match.objects.get(id=request.data.get("pk"))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该比赛",
                             }, status=status.HTTP_200_OK)

        if match.check != 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "审核通过比赛不允许修改",
                             }, status=status.HTTP_200_OK)

        match.type = Type.objects.get(id=request.data.get("type"))
        match.title = request.data.get("title")
        match.count = request.data.get("count")
        match.content = request.data.get("content")
        match.classes = request.data.get("classes")
        match.sign_endtime = request.data.get("sign_endtime")
        match.sign_starttime = request.data.get("sign_starttime")
        match.group_maxcount = request.data.get("group_maxcount")
        match.group_mincount = request.data.get("group_mincount")
        match.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class MatchPorocess(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    """比赛流程逻辑"""
    serializer_class = MatchProceessSerializer
    pagination_class = P1
    queryset = Match.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, TeacherPermission)
    def create(self,request,*args,**kwargs):
        """创建比赛流程"""
        # 校验参数
        serializer = MatchProceessSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        serializer.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def destory(self,request,*args,**kwargs):
        """删除比赛流程"""
        id = kwargs.get("pk",0)

        try:
            process = Process.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "找不到该流程",
                         }, status=status.HTTP_200_OK)
        process.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class TypeViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                       viewsets.GenericViewSet, mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    """分类逻辑"""

    serializer_class = TypeSerializer
    pagination_class = P1
    queryset = Type.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, TeacherPermission)

class NewsViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                       viewsets.GenericViewSet, mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    # 赛事新闻
    serializer_class = NewsSerializer
    pagination_class = P1
    queryset = News.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, TeacherPermission)
    def create(self, request, *args, **kwargs):
        # 校验参数
        serializer = NewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        News.objects.create(content=request.data["content"],title=request.data["title"])

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        # 校验参数
        serializer = NewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new = News.objects.get(id=kwargs.get("pk",0))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该新闻",
                             }, status=status.HTTP_200_OK)

        new.content = request.data["content"]
        new.title = request.data["title"]
        new.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

class TeacherMatchResultViewset(APIView):
    def post(self,request,*args,**kwargs):
        file = request.FILES.get('file',None)

        process = request.data.get("process", 0)

        if file is None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "未上传文件",
                             "results": [],
                             }, status=status.HTTP_200_OK)

        try:
            process = Process.objects.get(id=process)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "未找到文件",
                             "results": [],
                             }, status=status.HTTP_200_OK)

        # 如果比赛还没结束,不能上传
        if datetime.date.today() < process.endtime:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "未找到文件",
                             "results": "流程还没结束，不能上传成绩",
                             }, status=status.HTTP_200_OK)

        file_content = ContentFile(file.read())  # 创建ContentFile对象
        process.result.save(datetime.datetime.now().strftime("%Y%m%d%H%M%S.xls"), file_content)  # 保存文件到user的photo域
        process.save()
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

############ 普通用户逻辑
class SignMatchViewset(APIView):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, UserPermission)
    def post(self,request,*args,**kwargs):

        """报名"""
        match_id = request.data.get("match_id",None)

        userstr = request.data.get("userlist",None)

        userlist = userstr.split(",")

        try:
            match = Match.objects.get(id=match_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "找不到该比赛",
                         }, status=status.HTTP_200_OK)

        if match.check != 1:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该比赛",
                             }, status=status.HTTP_200_OK)

        if datetime.datetime.now() < match.sign_starttime:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results":"报名时间未到",
                         }, status=status.HTTP_200_OK)

        if datetime.datetime.now() > match.sign_endtime:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results":"报名已截至",
                         }, status=status.HTTP_200_OK)



        # 如果是个人赛
        if match.classes == 0:
            if len(match.user.all()) >= match.count: # 人数未满
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "人数已满",
                                 }, status=status.HTTP_200_OK)
            try:
                user = UserProfile.objects.get(id=request.user.id)
            except Exception as e:
                return Response({"status_code": status.HTTP_200_OK,
                                     "message": "ok",
                                     "results": "用户不存在",
                                     }, status=status.HTTP_200_OK)
            count = UseAndMatch.objects.filter(user=user,match=match).count()
            if count > 0:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "不能重复报名",
                                 }, status=status.HTTP_200_OK)

            UseAndMatch.objects.create(match=match,user=user)
            match.count += 1
            match.save()

        # 如果是团体赛
        else:

            if request.user.username not in userlist:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "你必须要在队伍中",
                                 }, status=status.HTTP_200_OK)

            if len(userlist) > match.group_maxcount or len(userlist) < match.group_mincount:
                return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "人数已满",
                         }, status=status.HTTP_200_OK)

            for index,name in enumerate(userlist):
                try:
                    user = UserProfile.objects.get(username=name)
                except Exception as e:
                    return Response({"status_code": status.HTTP_200_OK,
                                     "message": "ok",
                                     "results": "用户不存在",
                                     }, status=status.HTTP_200_OK)

                count = UseAndMatch.objects.filter(user=user, match=match).count()
                if count > 0:
                    return Response({"status_code": status.HTTP_200_OK,
                                     "message": "ok",
                                     "results": "不能重复报名",
                                     }, status=status.HTTP_200_OK)

                group = ",".join(userlist)
                if index == 0:
                    UseAndMatch.objects.create(match=match, user=user,group=group)
                else:
                    UseAndMatch.objects.create(match=match, user=user,is_leader=0,group=group)


        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        """查看自己比赛报名情况"""
        user_match = UseAndMatch.objects.filter(user=request.user,check=1).all().order_by("signtime")

        p1 = P1()
        page_list = p1.paginate_queryset(queryset=user_match, request=request, view=self)

        serializer = UserandMatchSerializer(instance=page_list,many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        """增加用户"""
        match_id = request.data.get("match_id")

        userstr =request.data.get("userlist") # 要删除的人
        userlist = list(set(userstr.split(",")))


        use_and_match = UseAndMatch.objects.filter(match=match_id,user=request.user).first()

        if use_and_match is None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法操作该报名",
                             }, status=status.HTTP_200_OK)

        if use_and_match.is_leader != 1 or use_and_match.check != 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法操作该报名",
                             }, status=status.HTTP_200_OK)

        # 如果是个人赛，直接取消
        if use_and_match.match.classes == 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "该比赛是个人赛",
                             }, status=status.HTTP_200_OK)
        # 团体赛判断删除的人
        else:
            # 现在的团对
            mygroup = use_and_match.group.split(",")

            if (len(mygroup) + len(userlist) ) > use_and_match.match.group_maxcount :
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "增加报名人数错误",
                                 }, status=status.HTTP_200_OK)

            newgroup = use_and_match.group
            for username in userlist:
                try:
                    user = UserProfile.objects.get(username=username)
                except Exception as e:
                    return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "无效用户",
                                 }, status=status.HTTP_200_OK)

                count = UseAndMatch.objects.filter(match=match_id,user=user).count()
                if count > 0:
                    return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": username+"用户已重复报名",
                                 }, status=status.HTTP_200_OK)
                # 增加报名
                UseAndMatch.objects.create(match=use_and_match.match,user=user,is_leader=0)

                newgroup = newgroup + "," + username

            # 跟新团队所有人的group
            for username in newgroup.split(","):
                UseAndMatch.objects.filter(user=UserProfile.objects.get(username=username),match=use_and_match.match).update(group=newgroup)



        return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": [],
                                 }, status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        """取消某比赛报名"""
        match_id = request.data.get("match_id")

        userstr =request.data.get("userlist") # 要删除的人
        userlist = userstr.split(",")


        use_and_match = UseAndMatch.objects.filter(match=match_id,user=request.user).first()

        if use_and_match is None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法取消该报名",
                             }, status=status.HTTP_200_OK)

        if use_and_match.is_leader != 1 or use_and_match.check != 0:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "你无法取消该报名",
                             }, status=status.HTTP_200_OK)

        # 如果是个人赛，直接取消
        if use_and_match.match.classes == 0:
            use_and_match.delete()
        # 团体赛判断删除的人
        else:
            # 现在的团对
            mygroup = use_and_match.group.split(",")


            if (len(mygroup) - len(userlist) ) < use_and_match.match.group_mincount and set(mygroup) != set(userlist):
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "取消报名人数错误",
                                 }, status=status.HTTP_200_OK)
            if request.user.username in userlist: # 如果删除名单里有队长，就把队伍解散
                for user in mygroup:
                    UseAndMatch.objects.filter(match=match_id, user=user).delete()

                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "队伍解散",
                                 }, status=status.HTTP_200_OK)


            for username in userlist:
                try:
                    user = UserProfile.objects.get(username=username)
                except Exception as e:
                    return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": username + "找不到",
                                 }, status=status.HTTP_200_OK)
                UseAndMatch.objects.filter(match=match_id,user=user).delete()

            # 组装跟新之后的group
            newgroup = ",".join(list(set(mygroup) - set(userlist)))

            for username in newgroup.split(","):
                UseAndMatch.objects.filter(user=UserProfile.objects.get(username=username),
                                           match=use_and_match.match).update(group=newgroup)


        return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": [],
                                 }, status=status.HTTP_200_OK)


class CommentViewset(viewsets.GenericViewSet):
    """用户评论逻辑"""

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, UserPermission)
    def create(self,request,*args,**kwargs):
        content = request.data.get("content",None)
        match_id = request.data.get("match",None)
        if content is None:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "不能提交空评论",
                         }, status=status.HTTP_200_OK)

        try:
            match = Match.objects.get(id=match_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该比赛",
                             }, status=status.HTTP_200_OK)
        if match.check != 1:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该比赛",
                             }, status=status.HTTP_200_OK)

        Comment.objects.create(match=match,user=request.user,content=content)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self,request,*args,**kwargs):
        """查看登录用户所有评论"""

        p1 = P1()
        p_comment = p1.paginate_queryset(Comment.objects.filter(user=request.user).order_by("starttime"),request=request, view=self)
        serializer = CommentSerializer(instance=p_comment,many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)

    def retrieve(self,request,*args,**kwargs):
        """查看某篇文章的评论"""
        match_id = request.data.get("match_id")

        try:
            match = Match.objects.get(id=match_id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": "找不到该比赛",
                         }, status=status.HTTP_200_OK)


        p1 = P1()
        p_comment = p1.paginate_queryset(Comment.objects.filter(user=request.user,match=match).order_by("starttime"),request=request, view=self)
        serializer = CommentSerializer(instance=p_comment, many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)



########### 其他
class TypeMatch(viewsets.GenericViewSet,mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """分类和比赛"""
    serializer_class = TypeMatchSerializer
    pagination_class = P1
    queryset = Type.objects.all()

class FindViewset(APIView):
    """搜索比赛"""
    def get(self,request,*args,**kwargs):
        query = request.GET.get("query")

        matchs = Match.objects.filter(title__contains=query,check=1).all().order_by("sign_endtime")

        p1 = P1()
        p_match = p1.paginate_queryset(matchs, request=request, view=self)
        serializer = DetailMatchSerializer(instance=p_match,many=True)


        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)


























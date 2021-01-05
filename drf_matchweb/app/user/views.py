
from django.contrib.auth.backends import ModelBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .seriailzers import UserCreateSerializer,UserModifySerializer,UserDetailSerializer,DpartMentSerializer
from app.user.models import UserProfile,Dpartment,Major
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from app.utils.permissions import AdminPermission,UserPermission
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

class AdminToUserViewset(APIView):
    """
    管理员对用户操作
    post:创建用户
    put: 修改用户
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    def post(self,request,*args,**kwargs):
        # 校验参数
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存
        serializer.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def put(self,request,*args,**kwargs):
        id = request.data.get("id",0)

        try:
            user = UserProfile.objects.get(id=id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "找不到该用户",
                         "results": [],
                         }, status=status.HTTP_200_OK)

        serializer = UserModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserProfile.objects.filter(id=id).update(**serializer.validated_data)
        # 额外修改密码
        if serializer.validated_data.get("password"):
            user.set_password(serializer.validated_data.get("password"))
            user.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        users = UserProfile.objects.all().order_by("role")

        p1 = P1()

        page_list = p1.paginate_queryset(queryset=users, request=request, view=self)

        user_Serializer = UserDetailSerializer(instance=page_list,many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results":{ "count":len(users),"users":[user_Serializer.data]},
                         }, status=status.HTTP_200_OK)




class AdminDetailUserViewset(APIView):
    """
    这里主要是管理员管理一个详细的用户信息
    get:获取一个用户详细信息
    delete:删除一个用户
    """
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated, AdminPermission)
    def get(self,request,*args,**kwargs):

        user_id = kwargs.get("id")
        try:
            user = UserProfile.objects.filter(id=int(user_id)).get()
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "参数错误",
                             "results": [],
                             }, status=status.HTTP_200_OK)

        ret = UserDetailSerializer(instance=user,many=False)
        ret = ret.data

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [ret],
                         }, status=status.HTTP_200_OK)


    def delete(self,request,*args,**kwargs):
        """删除详细用户"""
        id = kwargs.get("id")

        try:
            user = UserProfile.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                         "message": "error",
                         "results": "参数错误",
                         }, status=status.HTTP_200_OK)
        user.delete()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)



############# 上面是管理员逻辑

class UserViewset(APIView):
    """
    普通用户自己的操作
    get:获取登录用户信息
    put:修改用户信息
    """
    permission_classes = (IsAuthenticated, UserPermission)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    def get(self,request,*args,**kwargs):
        user_id = request.user.id
        try:
            user = UserProfile.objects.filter(id=int(user_id)).get()
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "参数错误",
                             "results": [],
                             }, status=status.HTTP_200_OK)

        ret = UserDetailSerializer(instance=user,many=False)
        ret = ret.data

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [ret],
                         }, status=status.HTTP_200_OK)


    def put(self,request,*args,**kwargs):


        serializer = UserModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)



        UserProfile.objects.filter(id=request.user.id).update(**serializer.validated_data)
        # 额外修改密码
        if serializer.validated_data.get("password"):
            request.user.set_password(serializer.validated_data.get("password"))
            request.user.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class MajorViewset(APIView):
    """专业逻辑"""

    def get(self,request,*args,**kwargs):
        depatments = Dpartment.objects.filter().all()

        dpartMent_serializer = DpartMentSerializer(instance=depatments,many=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [dpartMent_serializer.data],
                         }, status=status.HTTP_200_OK)
















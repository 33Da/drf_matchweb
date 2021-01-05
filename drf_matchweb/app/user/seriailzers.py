# -*- coding: utf-8 -*-

# Date: 2019/8/5
# Name: serializers


from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from app.user.models import UserProfile, Dpartment, Major
import datetime
import re

User = get_user_model()


def is_phone(phone):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, phone)
    if not res:
        return False
    return True


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """

    class Meta:
        model = User
        fields = ("id", "username", "last_name", "grade", "major", "department", "email", "phone", "role")


class UserCreateSerializer(serializers.Serializer):
    """
    添加用户序列化类
    """

    username = serializers.CharField(max_length=10, min_length=10, error_messages={"required": "学号不能为空"},
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="学号存在了")])

    password = serializers.CharField(error_messages={"required": "不能为空"}, style={'input_type': 'password'},
                                     help_text="密码", label="密码", write_only=True)

    last_name = serializers.CharField(max_length=10, error_messages={"required": "不能为空"}, help_text="姓名", label="姓名",
                                      write_only=True)

    role = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="角色", label="角色")

    def validate(self, data):
        if int(data["role"]) not in [1, 0, 2]:
            raise serializers.ValidationError("角色信息错误")

        return data

    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserModifySerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=10, help_text="姓名", label="姓名",required=False
                                      )

    grade = serializers.CharField(max_length=4, help_text="年级", label="年级",required=False
                                  )

    major = serializers.CharField(max_length=10, help_text="专业", label="专业",required=False
                                  )

    department = serializers.CharField(max_length=10, help_text="学院", label="学院",required=False
                                       )

    phone = serializers.CharField(help_text="手机号", label="手机号",required=False
                                  )

    email = serializers.EmailField(help_text="email", label="email",required=False
                                   )

    password = serializers.CharField(style={'input_type': 'password'},
                                     help_text="密码", label="密码", write_only=True,required=False)

    def validate(self, data):
        def validate(self, data):
            # 获取当前年
            year = datetime.datetime.now().year

            # 生成年份列表
            year_list = [i for i in range(1985, int(year) + 1)]

            if int(data.get("grade")) and data.get("grade") not in year_list:
                raise serializers.ValidationError("年级信息错误")

            if data.get("department"):
                try:
                    Dpartment.objects.get(id=data["department"])
                except Exception as e:
                    print(e)
                    raise serializers.ValidationError("部门信息错误")

            if data.get("major"):
                try:
                    Major.objects.get(id=data["major"])
                except Exception as e:
                    raise serializers.ValidationError("专业信息错误")

            if data.get("phone"):
                if not is_phone(data["phone"]):
                    raise serializers.ValidationError("手机号错误")

        return data


class AdminModifySerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, min_length=10,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="学号存在")],required=False)

    last_name = serializers.CharField(max_length=10, help_text="姓名", label="姓名",required=False
                                      )

    grade = serializers.CharField(max_length=4, help_text="年级", label="年级",required=False
                                  )

    major = serializers.CharField(max_length=10, help_text="专业", label="专业",required=False
                                  )

    department = serializers.CharField(max_length=10, help_text="学院", label="学院",required=False
                                       )

    phone = serializers.CharField(help_text="手机号", label="手机号",required=False)

    role = serializers.CharField(help_text="角色", label="角色", required=False)

    email = serializers.EmailField(help_text="email", label="email",required=False)

    password = serializers.CharField(style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,required=False)

    def validate(self, data):
        # 获取当前年
        year = datetime.datetime.now().year

        # 生成年份列表
        year_list = [i for i in range(1985, int(year) + 1)]

        if int(data.get("grade")) and data.get("grade") not in year_list:
            raise serializers.ValidationError("年级信息错误")

        if data.get("department"):
            try:
                Dpartment.objects.get(id=data["department"])
            except Exception as e:
                print(e)
                raise serializers.ValidationError("部门信息错误")

        if data.get("major"):
            try:
                Major.objects.get(id=data["major"])
            except Exception as e:
                raise serializers.ValidationError("专业信息错误")

        if data.get("phone"):
            if not is_phone(data["phone"]):
                raise serializers.ValidationError("手机号错误")


        return data


class MajorSerializer(serializers.ModelSerializer):
    """获取所有部门"""

    class Meta:
        model = Major
        fields = ("id", "name")


class DpartMentSerializer(serializers.ModelSerializer):
    """获取所有部门"""

    major = MajorSerializer(many=True)

    class Meta:
        model = Dpartment
        fields = ("id", "name", "major")

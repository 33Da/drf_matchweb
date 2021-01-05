# -*- coding: utf-8 -*-

# Date: 2019/8/5
# Name: serializers


from rest_framework import serializers,exceptions
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from app.match.models import Match,Type,Process,UseAndMatch,Comment,News
from app.user.models import UserProfile
import datetime
from app.user.seriailzers import UserDetailSerializer



class CreateMatchSerializer(serializers.Serializer):
    """
    创建比赛序列化类
    """
    title = serializers.CharField(min_length=1, max_length=100, error_messages={"required": "竞赛名不能为空"},
                                     validators=[UniqueValidator(queryset=Match.objects.all(), message="竞赛存在")])

    content = serializers.CharField(error_messages={"required": "不能为空"},help_text="竞赛内容", label="竞赛内容")

    sign_starttime = serializers.DateField( error_messages={"required": "不能为空"}, help_text="报名日期", label="报名日期")

    sign_endtime = serializers.DateField(error_messages={"required": "不能为空"}, help_text="报名截至日期", label="报名截至日期")

    count = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="报名人数", label="报名人数")

    type = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="比赛类型", label="比赛类型")

    classes = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="比赛种类", label="比赛种类")

    group_maxcount = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="最大人数", label="最大人数")

    group_mincount = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="最小人数", label="最小人数")


    def validate(self, data):
        try:
            Type.objects.get(id=data["type"])
        except Exception as e:
            raise serializers.ValidationError("没有这个比赛种类")

        if data["sign_starttime"] > data["sign_endtime"]:
            raise serializers.ValidationError("报名时间不得大于报名截至日期")

        if data["classes"] not in [1,0]:
            raise serializers.ValidationError("比赛种类不合法")

        return data


class MatchProceessSerializer(serializers.Serializer):
    """
    比赛流程序列化
    """
    id = serializers.CharField(read_only=True)

    name = serializers.CharField(max_length=60,min_length=1,error_messages={"required": "学号不能为空"})

    starttime = serializers.DateField(error_messages={"required": "不能为空"}, help_text="开始日期", label="开始日期")

    endtime = serializers.DateField(error_messages={"required": "不能为空"}, help_text="结束日期", label="结束日期")

    match = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="比赛", label="比赛",write_only=True)

    result = serializers.CharField(read_only=True)
    def validate(self, data):
        try:
            match = Match.objects.get(id=data["match"])
        except Exception as e:
            raise serializers.ValidationError("找不到比赛")

        return data


    def create(self, validated_data):

        validated_data["match"] = Match.objects.get(id=validated_data["match"])


        process = Process.objects.create(**validated_data)

        return process

class UpdataMatchSerializer(serializers.Serializer):
    """
    跟新比赛序列化类
    """
    title = serializers.CharField(min_length=1, max_length=100, error_messages={"required": "竞赛名不能为空"})

    content = serializers.CharField(error_messages={"required": "不能为空"},help_text="竞赛内容", label="竞赛内容")

    sign_starttime = serializers.DateField( error_messages={"required": "不能为空"}, help_text="报名日期", label="报名日期")

    sign_endtime = serializers.DateField(error_messages={"required": "不能为空"}, help_text="报名截至日期", label="报名截至日期")

    count = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="报名人数", label="报名人数")

    type = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="比赛类型", label="比赛类型")

    classes = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="比赛种类", label="比赛种类")

    group_maxcount = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="最大人数", label="最大人数")

    group_mincount = serializers.IntegerField(error_messages={"required": "不能为空"}, help_text="最小人数", label="最小人数")

    def validate(self, data):
        try:
            Type.objects.get(id=data["type"])
        except Exception as e:
            raise serializers.ValidationError("没有这个比赛种类")

        if data["sign_starttime"] > data["sign_endtime"]:
            raise serializers.ValidationError("报名时间不得大于报名截至日期")

        if data["classes"] not in [1,0]:
            raise serializers.ValidationError("比赛种类不合法")

        return data

class TypeSerializer(serializers.ModelSerializer):
    """比赛分类"""
    class Meta:
        model = Type
        fields = "__all__"

class TypeMatchSerializer(serializers.ModelSerializer):
    """比赛分类"""
    match = serializers.SerializerMethodField(read_only=True)

    def get_match(self,row):
        matchs = []
        for match in row.match.all():
            # 如果比赛过了审核 并且报名时间还没到
            if match.check == 1 and match.sign_endtime > datetime.datetime.now():
                matchs.append({"id":match.id,"name":match.title})

        return matchs
    class Meta:
        model = Type
        fields = "__all__"


class DetailMatchSerializer(serializers.ModelSerializer):
    """
   比赛序列化类
    """
    process = MatchProceessSerializer(many=True)

    user = UserDetailSerializer(many=True)

    group = serializers.SerializerMethodField()

    def get_group(self,row):
        # 所有队长
        leaders = UseAndMatch.objects.filter(match=row,is_leader=1,group__isnull=False).all()

        groups = []
        for leader in leaders:

            group = []
            userlist = leader.group.split(",")
            for user in userlist:
                user = UserProfile.objects.get(username=user)
                group.append({"username":user.username,"id":user.id})
            groups.append(group)


        return groups

    class Meta:
        model = Match
        fields = "__all__"


class UserandMatchSerializer(serializers.ModelSerializer):
    match = serializers.SerializerMethodField()

    group = serializers.SerializerMethodField()

    def get_group(self, row):
        # 所有队长

        groups = []

        userlist = row.group.split(",")
        for user in userlist:
            user = UserProfile.objects.get(username=user)
            groups.append({"username": user.username, "id": user.id})

        return groups


    def get_match(self,row):

        # match = Match.objects.get(id=row.match.id)

        return {"id":row.match.id,"title":row.match.title}

    class Meta:
        model = UseAndMatch
        fields = ("id","is_leader","signtime","user","match","group","check")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

class NewsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60, min_length=1, error_messages={"required": "标题不能为空"}, help_text="标题", label="标题")

    content = serializers.CharField(error_messages={"required": "内容不能为空"}, help_text="内容", label="内容")

    starttime = serializers.DateTimeField(read_only=True)

    id = serializers.CharField(read_only=True)








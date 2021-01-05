from django.db import models
from DjangoUeditor.models import UEditorField
from app.user.models import UserProfile
import datetime

class Type(models.Model):
    """比赛种类"""

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "比赛种类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Match(models.Model):
    """比赛表"""
    CLASSES = (
        (0, "单人赛"),
        (1, "团体赛"),

    )

    CHECK = (
        (0,"待审核"),
        (1,"审核通过"),
        (2,"审核不通过")

    )

    title = models.CharField(max_length=100,verbose_name="标题",help_text="标题")

    content = UEditorField(verbose_name="竞赛内容", help_text="竞赛内容", null=True, blank=True,filePath='ueditor/file/',imagePath='ueditor/images/')

    sign_starttime = models.DateTimeField(verbose_name="报名开始时间", help_text="报名开始时间")

    sign_endtime = models.DateTimeField(verbose_name="报名结束时间", help_text="报名结束时间")

    count = models.IntegerField(verbose_name="报名人数", help_text="报名人数")

    group_maxcount = models.IntegerField(default=0,verbose_name="最大队内人数", help_text="最大队内人数")

    group_mincount = models.IntegerField(default=0, verbose_name="最小队内人数", help_text="最小队内人数")

    type = models.ForeignKey(Type,on_delete=models.CASCADE,verbose_name="比赛类型", help_text="比赛类型",related_name="match")

    classes = models.IntegerField(choices=CLASSES,verbose_name="比赛种类", help_text="比赛种类")

    user = models.ManyToManyField(UserProfile, through="UseAndMatch", related_name="my_match", help_text="报名人",
                                  verbose_name="报名人", blank=True, null=True)

    check = models.IntegerField(choices=CHECK,verbose_name="审核状态",help_text="审核状态")


    class Meta:
        verbose_name = "竞赛"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Process(models.Model):
    """比赛流程表"""
    name = models.CharField(max_length=100,verbose_name="流程名",help_text="流程名")

    starttime = models.DateField(verbose_name="流程开始时间", help_text="流程开始时间")

    endtime = models.DateField(verbose_name="流程结束时间", help_text="流程结束时间")

    match = models.ForeignKey(Match,verbose_name="比赛", help_text="比赛",related_name="process",on_delete=models.CASCADE)

    result = models.FileField(verbose_name="比赛结果", help_text="比赛结果", blank=True, null=True, upload_to="file/")

    class Meta:
        verbose_name = "比赛流程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.match + "-"+self.name


class News(models.Model):
    """新闻"""
    title = models.CharField(max_length=120,verbose_name="标题", help_text="标题")

    content = UEditorField(verbose_name="新闻内容", help_text="新闻内容", null=True, blank=True,filePath='ueditor/file/',imagePath='ueditor/images/')

    starttime = models.DateTimeField(default=datetime.datetime.now, verbose_name="创建时间", help_text="创建时间")

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UseAndMatch(models.Model):
    """用户比赛关系表"""
    LEADER = (
        (0, "不是队长"),
        (1, "是队长"),
    )

    CHECK = (
        (0, "待审核"),
        (1, "审核通过"),
        (2, "审核不通过")

    )

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户", help_text="用户")

    match = models.ForeignKey(Match,on_delete=models.CASCADE,verbose_name="比赛", help_text="比赛")

    is_leader = models.IntegerField(choices=LEADER,default=1)

    signtime = models.DateTimeField(default=datetime.datetime.now, verbose_name="报名时间", help_text="报名时间")

    group = models.CharField(max_length=300,blank=True,null=True,verbose_name="小组", help_text="小组")

    check = models.IntegerField(choices=CHECK, default=0, verbose_name="审核状态", help_text="审核状态")

class Comment(models.Model):
    """评论表"""

    CHECK = (
        (0, "待审核"),
        (1, "审核通过"),
        (2, "审核不通过")

    )

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="评论用户", help_text="评论用户",related_name="comment")

    starttime = models.DateTimeField(default=datetime.datetime.now, verbose_name="评论时间", help_text="评论时间")

    check = models.IntegerField(choices=CHECK, default=0, verbose_name="审核状态", help_text="审核状态")

    content = UEditorField(verbose_name="评论内容", help_text="评论内容", null=True, blank=True,filePath='ueditor/file/',imagePath='ueditor/images/')

    match = models.ForeignKey(Match,on_delete=models.CASCADE,verbose_name="评论竞赛", help_text="评论竞赛",default=1,related_name="comment")
    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content




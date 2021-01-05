from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.



class Dpartment(models.Model):
    """学院"""
    name = models.CharField(max_length=11, verbose_name="学院", help_text="学院", default="")

    class Meta:
        verbose_name = '学院'
        verbose_name_plural = verbose_name



class Major(models.Model):
    """专业"""
    name = models.CharField(max_length=30, verbose_name="专业名",help_text="专业名", default="")

    department = models.ForeignKey(Dpartment,on_delete=models.CASCADE,default=models.CASCADE,verbose_name="学院", help_text="学院",related_name="major")

    class Meta:
        verbose_name = '专业'
        verbose_name_plural = verbose_name





class UserProfile(AbstractUser):
    """
    用户表
    """
    ROLE_TYPE = (
        (0, "普通用户"),
        (1, "教职工"),
        (2, "管理员"),
    )

    role = models.IntegerField(choices=ROLE_TYPE, verbose_name="角色", help_text="角色",
                                default=0)

    major = models.ForeignKey(Major,on_delete=models.CASCADE,verbose_name="专业", help_text="专业",related_name="user",blank=True,null=True)

    department = models.ForeignKey(Dpartment,on_delete=models.CASCADE,verbose_name="学院", help_text="学院",related_name="user",blank=True,null=True)

    phone = models.CharField(max_length=11, verbose_name="手机",help_text="手机", default="")

    grade = models.CharField(max_length=4, verbose_name="年级",help_text="年级", default="")



    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username




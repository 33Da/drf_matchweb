# -*- coding: utf-8 -*-

# Date: 2019/8/8
# Name: permissions


from rest_framework import permissions


import re


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    是否是超级管理员
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser == 1




class UserPermission(permissions.BasePermission):
    """
    用户访问权限控制管理
    """
    message = "对不起，你没有权限"

    def has_permission(self, request, view):
        """
        检测用户访问权限
        :param request:
        :param view:
        :return:
        """

        if request.user.role >= 0:
            return True
        else:
            return False



class TeacherPermission(permissions.BasePermission):
    """
    用户访问权限控制管理
    """
    message = "对不起，你没有权限"

    def has_permission(self, request, view):
        """
        检测用户访问权限
        :param request:
        :param view:
        :return:
        """

        if request.user.role >= 1:
            return True
        else:
            return False

class AdminPermission(permissions.BasePermission):
    """
    用户访问权限控制管理
    """
    message = "对不起，你没有权限"

    def has_permission(self, request, view):
        """
        检测用户访问权限
        :param request:
        :param view:
        :return:
        """

        if request.user.role >= 2:
            return True
        else:
            return False
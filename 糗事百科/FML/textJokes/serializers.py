'''
Created on 2020-05-18 09:59
@description
@author mac
@name serializers
'''
from rest_framework import serializers
from textJokes.models import Story

class StorySerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似
    class Meta:
        model = Story
        # 和"__all__"等价
        fields = '__all__'
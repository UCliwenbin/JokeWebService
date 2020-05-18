from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from textJokes.models import Story
from .serializers import StorySerializer


def index(request):
    return HttpResponse('欢迎来到我的界面')

#获取所有数据
@api_view(['GET'])
def data(request):
    #查询数据库
    if request.method == 'GET':
        story_list = Story.objects.all()
        serializer = StorySerializer(story_list,many=True)
        return Response(serializer.data)

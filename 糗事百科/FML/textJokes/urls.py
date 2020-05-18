'''
Created on 2020-05-18 09:34
@description
@author mac
@name urls
'''

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('data/',views.data,name='data'),
]
from django.urls import path
from file_exchanger.views import MouseFormView, MouseListView, oops

urlpatterns = [

    path('', MouseFormView.as_view(), name='main'),
    path('oops', oops, name='oops'),
    path('up/<str:set_id>', MouseListView.as_view(), name='list'),
]
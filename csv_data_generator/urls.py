from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('newschema/', views.NewSchemaView.as_view(), name='newschema'),
]

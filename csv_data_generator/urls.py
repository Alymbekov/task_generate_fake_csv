from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexSchemaView.as_view(), name='index-schema'),
    path('newschema/', views.NewSchemaView.as_view(), name='newschema'),
    path('newschema/<int:pk>/', views.SchemaDetailView.as_view(), name='schema-detail'),
]

from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cats', views.CatViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    # path(r'api/', include(router.urls)),
    # path('<int:cat_id>/', views.cat_info, name='cat_info'),
    path(r'api/v1/cat/<int:pk>', views.cat_endpoint, name='cat_endpoint'),
    path(r'api/v1/cats/', views.cats_endpoint, name='cats_endpoint'),
    path(r'api/v1/details/', views.details_endpoint, name='details_endpoint'),
    path('accounts/', include('django.contrib.auth.urls')),
]

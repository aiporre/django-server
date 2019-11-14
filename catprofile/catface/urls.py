from django.urls import path, include
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cats', views.CatViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path(r'about/',TemplateView.as_view(template_name="catface/about.html")),
    # path(r'api/', include(router.urls)),
    # path('<int:cat_id>/', views.cat_info, name='cat_info'),
    path(r'api/v1/cat/<int:pk>', views.cat_endpoint, name='cat_endpoint'),
    path(r'api/v1/mostliked/', views.most_liked, name='most_liked'),
    path(r'api/v1/tumbup/<int:pk>', views.tumbup, name='tumbup'),
    path(r'api/v1/cats/', views.cats_endpoint, name='cats_endpoint'),
    path(r'api/v1/details/', views.details_endpoint, name='details_endpoint'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(r'signup/', views.signup, name='signup'),
    path(r'search/', views.SearchResultsView.as_view(), name='search_results'),


]

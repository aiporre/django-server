from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
# Create your views here.

from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cat, Details
from .serializers import CatSerializer, DetailsSerializer, CatDetailsSerializer
# Serialized views:

class CatDetailsViewSet(viewsets.ModelViewSet):
    querySet = Details.objects.all()
    serializer_class = CatDetailsSerializer

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

# views: dynamic pure django view
def index(request):
    all_cats = Cat.objects.all()
    template = loader.get_template('catface/home.html')
    context = {
        # 'cat_list' : all_cats,
    }
    return HttpResponse(template.render(context, request))
def cat_info(request, cat_id):
    c = get_object_or_404(Cat, pk=cat_id)
    return render(request, 'catface/cat_info.html', {'name': c})

# views: api django rest_framework
@api_view(['GET'])
def cat_endpoint(request, pk):
    '''
    Endpoint to single cat
    :param request: request object
    :param pk: id in DB:
    :return: HTTP response
    '''
    try:
        cat = Cat.objects.get(pk=pk)
    except Cat.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serialized = CatSerializer(cat)
        return Response(serialized.data)

@api_view(['GET'])
def cats_endpoint(request):
    ''' Endpoint to list of cats
    :param request: request object
    :return: HTTP response
    '''
    if request.method == 'GET':
        cats = Cat.objects.all()
        serialized = CatSerializer(cats, many=True)
    return Response(serialized.data)

@api_view(['GET'])
def details_endpoint(request):
    ''' Endpoint to list of cats and details
    :param request: request object
    :return: HTTP response
    '''
    if request.method == 'GET':
        # cats = Cat.objects.all()
        details = Details.objects.all()
        serialized = CatDetailsSerializer(details, many=True)
    return Response(serialized.data)

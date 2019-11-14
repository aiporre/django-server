from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect

# Create your views here.
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cat, Details
from .serializers import CatSerializer, DetailsSerializer, CatDetailsSerializer
from .forms import SignUpForm
# ---
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q


# Serialized views:

class CatDetailsViewSet(viewsets.ModelViewSet):
    querySet = Details.objects.all()
    serializer_class = CatDetailsSerializer

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

# class views:
class SearchResultsView(ListView):
    model = Details
    # querySet = Details.objects.all()
    # serializer_class = CatDetailsSerializer
    template_name = 'catface/searchresults.html'
    def get_queryset(self): # new
        query = self.request. GET.get('q')
        if query is None:
            query = ''
        print('query: ', query)
        details = Details.objects.all()
        serialized = CatDetailsSerializer(details, many=True)
        object_list = [d for d in serialized.data if query in d['cat']['cat_name']]
        return object_list

# views: dynamic pure django view
# def about(request):
#     template = loader.get_template('catface/about.html')
#     return HttpResponse(template.render(request))

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

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print('USER CREATED:')
            return redirect('/')
    else:
        form = SignUpForm()
    print("THIS IS NOT A POST")
    return render(request, 'catface/signup.html', {'form': form})

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
def most_liked(request):
    ''' Endpoint to list of cats with the highes cat
    :param request: request object
    :return: HTTP response
    '''
    if request.method == 'GET':
        cats = Details.objects.all().order_by('likes')
        print('cats.data: ', cats)
        serialized = CatDetailsSerializer(cats, many=True)
        return Response(serialized.data)

@api_view(['GET','POST'])
def tumbup(request,pk):
    '''
    endpoint to tumbup a cat
    '''
    if request.method == 'POST':
        try:
            d = Details.objects.get(pk=pk)
            likes = d.likes+1
            Details.objects.filter(pk=pk).update(likes = likes)
        except Cat.DoesNotExist:
            return HttpResponse(status=404)
        serialized = DetailsSerializer(d)
        return redirect('/search/')




@api_view(['GET', 'POST'])
def cats_endpoint(request):
    ''' Endpoint to list of cats
    :param request: request object
    :return: HTTP response
    '''
    if request.method == 'GET':
        cats = Cat.objects.all()
        serialized = CatSerializer(cats, many=True)
        return Response(serialized.data)
    elif request.method == 'POST':
        print('Creating cat')
        catSerializer = CatSerializer(data=request.data)
        print('request.data',request.data)
        if catSerializer.is_valid():
            catSerializer.save()
            print('cat created',catSerializer.data)
            print(dir(request.data))
            print(request.data.__class__)
            # if not isinstance(request.data,dict):
            #     print('it is not a dict converting to dict')
            #     request_data = request.data.dict
            # else:
            #     print('it is a dict using the input directoy')
            #     request_data = request.data
            request_data = request.data.copy()
            request_data['cat']= catSerializer.data.get('id')
            print(request_data.__class__)
            print(request_data)
            detailsSerializer = DetailsSerializer(data=request_data)
            if detailsSerializer.is_valid():
                detailsSerializer.save()
                print('details for cat',detailsSerializer.data)
                render(request, 'catface/cat_info.html', {'cat_name': request_data['cat_name']})
                return redirect('/') #Response(catSerializer.data, status=status.HTTP_201_CREATED)
        return Response(catSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

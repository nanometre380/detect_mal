from django.shortcuts import render, get_object_or_404
from .models import Black, White
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import BlackSerializer, WhiteSerializer
import json
from bs4 import BeautifulSoup
import urllib.request
import requests
import json

class BlackViewSet(viewsets.ModelViewSet):
    """
    API endpoints that allows users to be viewed or edited.
    """
    queryset = Black.objects.all()
    serializer_class = BlackSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field='url'

class WhiteViewSet(viewsets.ModelViewSet):
    """
    API endpoints that allows users to be viewed or edited.
    """
    queryset = White.objects.all()
    serializer_class = WhiteSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field='url'
    # def retrieve_url(self, request, url=None):
    #     queryset = White.objects.all()
    #     white = get_object_or_404(queryset, url=url)
    #     serializer = WhiteSerializer(white)
    #     return Response(serializer.data)


# Create your views here.

def home(request):
    return render(request, 'index.html')

#@api_view(['GET'])
def black_list(request):
    apikey = '853a551ae6d19cfa01e82e1f9a5f8dc31709e14ab173bcff5c62c35d53bce734'
    url = "http://data.phishtank.com/data/"+apikey+"/online-valid.json"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    black_last = Black.objects.last()
    if(rescode == 200):
        response_body = response.read()
        result = json.loads(response_body)
        for element in result:
            phish_id = element['phish_id']
            url = element['url']
            if(black_last.black_id < phish_id):    
                black = Black()
                black.black_id = phish_id
                black.url = str(url)
                black.save()

def white_list(request):
    catagory=['Adult', 'Arts', 'Business', 'Computers','Games','Reference','Regional','Science','Shopping','Society','Health','Home','Kids_and_Teens','News','Recreation','Sports' ]
    for kind in catagory:
        req=requests.get('https://www.alexa.com/topsites/category/Top/'+kind)
        html=req.text
        soup=BeautifulSoup(html, "html.parser", from_encoding='utf-8')
        pkg_list=soup.findAll("div","td DescriptionCell")

        for i in pkg_list: 
            title=i.findAll('a')
            whiteUrl=str(title)[str(title).find('siteinfo/')+9:str(title).find('">')]
            insert_white(whiteUrl)

def insert_white(whiteUrl):
    white = White()
    whiteUrl = "https://www."+whiteUrl
    white.url= whiteUrl
    white.save()

def check_url(request, url):
    flag_black=0
    try:
        value = get_object_or_404(White, url=url)
        flag_white = 1
    except:
        flag_white = 0
        try:
            value2 = get_object_or_404(Black, url=url)
            flag_black = 1
        except:
            flag_black = 0

    #value2 = get_object(Black,)
    
    if(flag_white == 1):
        result_check = 'green'
    elif(flag_white == 0 and flag_black == 1):
        result_check = 'red'
    else :
        result_check = 'orange'
    
    return render(request, 'result.html', {'result_check' : result_check, 'url' : url, 'flag_white' : flag_white, 'flag_black' : flag_black})
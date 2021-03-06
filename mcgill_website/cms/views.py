from cms.models import *
from rest_framework import status
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.http import JsonResponse
from cms.serializers import *
from django.views.decorators.clickjacking import xframe_options_exempt
import os
from unidecode import unidecode

#l2_page, l3_page: model reference ; language: string 'en' or 'fr'
def make_navbar_content(l2_page,l3_page,language):
    page_name_attr = 'page_name_'+language
    page_title_attr = 'page_title_'+language
    page_content_attr = 'page_content_'+language
    custom_js_css_attr = 'custom_js_css_'+language

    l2_to_add = Page.objects.get(page_name_en="home").children.all()
    navbar_content = []
    for i in l2_to_add:
        l2_at_current = l2_page==i
        l3_pages = []
        for j in i.children.all():
            l3_at_current = l3_page==j
            l3_pages.append({'l3_name':getattr(j,page_title_attr),'l3_link':'/'+language+'/'+getattr(i,page_name_attr)+'/'+getattr(j,page_name_attr),'is_current':l3_at_current})
        navbar_content.append({'l2_name':getattr(i,page_title_attr),'l2_link':'/'+language+'/'+getattr(i,page_name_attr),'is_current':l2_at_current,'l3_items':l3_pages})
    return navbar_content

args_base_params = {'Template': Template}
args_404 = {**args_base_params, 'template': Template.NO_SIDEBAR, 'title': '404 Not Found', 'content':'The page requested does not exist. La page demandée n\'existe pas.', 'custom_js_css': '','current_language':'en','other_language_link':'/fr'}

def render_404(request):
    return render(request,'base.html',{**args_404,'navbar_content':make_navbar_content(None,None,'en')})

# Create your views here.
def cms_view(request):
    path_list = os.path.normpath(request.path).split(os.path.sep) #parse path into a list
    language = path_list[1] #need to add something to handle the situation where a user types the path / without en or fr
    path_list = path_list[2:] 
    
    if request.path=='/': #if the user only typed the domain without following it with /en or /fr, then load the English home page
        language = 'en'
        path_list = []

    if language!='en' and language!='fr':
        return render_404(request)

    other_language = 'en' if language=='fr' else 'fr'
    page_name_attr = 'page_name_'+language
    page_title_attr = 'page_title_'+language
    page_content_attr = 'page_content_'+language
    custom_js_css_attr = 'custom_js_css_'+language
    #Find the page specified by the path by traversing the database in a tree-like manner starting from home
    #We start from the home page. The home page must have page_name_en = 'home'
    cur = Page.objects.filter(page_name_en='home')[0]
    not_found = False
    #For each next level specified in the path, match with one of the children of the current node. not_found becomes true because such a node is not found
    l2_page = None
    l3_page = None
    level = 2
    other_language_path = '/'+ other_language
    for dir in path_list:
        if language=="en":
            temp = cur.children.filter(page_name_en=dir)
        elif language=="fr":
            temp = cur.children.filter(page_name_fr=dir)

        if len(temp)> 0:
            cur = temp[0]
            other_language_path += '/'+ getattr(cur,'page_name_'+other_language)
            if level == 2:
                l2_page = cur
            if level == 3:
                l3_page = cur
            level = level + 1    

        else:
            not_found = True
            break

    navbar_content = make_navbar_content(l2_page,l3_page,language)
    serializer = SiteStructureSerializer(l2_page)
    if not_found:
        return render_404(request)
    else:
        args = {**args_base_params,
        'id': cur.id,
        'template':cur.page_template,
        'title': getattr(cur,page_title_attr),
        'content': getattr(cur,page_content_attr),
        'custom_js_css': getattr(cur,custom_js_css_attr),
        'current_language': language,
        'other_language_link': other_language_path,
        'navbar_content': navbar_content,
        'l2_page': serializer.data
        }
        return render(request,'base.html',args)

@xframe_options_exempt
def calendar_widget(request, language):
    all_events = Event.objects.all()
    return render(request,'calendar.html',{'events': all_events, 'language': language})

def job_posting_widget(request, language):
    latest = Job.objects.last()
    return render(request, 'job_posting_home.html', {'language': language, 'latest': latest})

def news_widget(request):
    return render(request, 'news.html')

def news_list(request):
    path_list = os.path.normpath(request.path).split(os.path.sep)
    tab = path_list[-1]
    if tab == 'news':
        current_language = 'en'
    elif tab == 'nouvelles':
        current_language = 'fr'
    news = News.objects.all().order_by()
    return render(request, 'news_list.html',{'news': news, 'current_language': current_language})

@api_view(['GET'])
def cms_editor_client_get_tree(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            serializer = SiteStructureSerializer(Page.objects.get(page_name_en='home'))
            return Response(serializer.data)
        return HttpResponse("You are not logged in.",status=403)
    return HttpResponse("You are not using GET",status=405)

@api_view(['POST'])
def cms_editor_create_page(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            serializer = PageCreationSerializer(data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse("You are not logged in.",status=403)
    else:
        return HttpResponse("Wrong method.",status=400)

@api_view(['POST'])
def cms_editor_client_edit_page(request,page_id):
    if request.method == "POST":
        if request.user.is_authenticated:
            page = Page.objects.get(id=page_id)
            serializer = SiteStructureSerializer(page,data=request.data,partial=True)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse("You are not logged in.",status=403)
    else:
        return HttpResponse("Wrong method.",status=400)

@api_view(['DELETE'])
def cms_editor_client_delete_page(request,page_id):
    if request.method == "DELETE":
        if request.user.is_authenticated:
            Page.objects.get(id=page_id).delete()
            return HttpResponse("Page successfully deleted.",status=200)
        else:
            return HttpResponse("You are not logged in.",status=403)
    else:
        request.HttpResponse("Wrong method.",status=400)

#the settings should be really short and just one object. Easier to do it directly than with serializers.
@api_view(['POST'])
def cms_editor_update_settings(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = request.data
            if(IBMCredential.objects.count()==0):
                credential = IBMCredential(api_key=data['ibm_api_key'],url=data['ibm_api_url'],version=data['ibm_api_version'])
                credential.save()
                return HttpResponse(status=200)
            else:
                credential = IBMCredential.objects.all()[0]
                credential.api_key = data['ibm_api_key']
                credential.url = data['ibm_api_url']
                credential.version = data['ibm_api_version']
                credential.save()
                return HttpResponse(status=200)
        else:
            return HttpResponse("You are not logged in.",status=403)
    else:
        return request.HttpResponse("Wrong method.",status=400)

@api_view(['GET'])
def cms_editor_get_settings(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            if IBMCredential.objects.count()==0:
                return JsonResponse({})
            credential = IBMCredential.objects.all()[0]
            return JsonResponse({'ibm_api_key': credential.api_key,'ibm_api_url': credential.url, 'ibm_api_version': credential.version})
        else:
            return HttpResponse("You are not logged in.",status=403)
    else:
        return request.HttpResponse("Wrong method.",status=400)



def cms_editor_view(request):
    return render(request,'editor.html')

def employment(request, section):
    path_list = os.path.normpath(request.path).split(os.path.sep)
    tab = path_list[-2]
    if tab == 'employment':
        current_language = 'en'
    elif tab == 'emploi':
        current_language = 'fr'
    if current_language == 'en':
        all_jobs = list(filter(lambda i: unidecode(i.english_section)==section,list(Job.objects.all())))
        sections = Job.objects.values_list('english_section', flat=True).distinct()
        url_sections = [unidecode(j) for j in list(sections.values_list('english_section', flat=True))]
    elif current_language == 'fr':
        all_jobs = list(filter(lambda i: unidecode(i.french_section)==section,list(Job.objects.all())))
        sections = Job.objects.values_list('french_section', flat=True).distinct()
        url_sections = [unidecode(j) for j in list(sections.values_list('french_section', flat=True))]
    length = len(all_jobs) + 1
    heading = []
    collapse = []
    for i in range(1, length):
        heading.append('heading' + str(i))
        collapse.append('collapse' + str(i))
    return render(request, 'employment.html', {'current_language': current_language, 'tab': tab, 'sections': sections, 'url_sections': url_sections ,'jobs': all_jobs, 'heading': heading, 'collapse': collapse})

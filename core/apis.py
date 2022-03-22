from core.models import Page, PageLink
from core.serializers import PageCommentSerializer, PageDownloadSerializer, PageImageSerializer, PageLinkSerializer, ParameterSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import PageCommentRepo, PageLinkRepo, PageRepo,  ParameterRepo,PageDownloadRepo,PageImageRepo
from .constants import SUCCEED, FAILED
from utility.utils import str_to_html

class ChangeParameterApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            change_parameter_form = ChangeParameterForm(request.POST)
            if change_parameter_form.is_valid():
                log += 1
                cd=change_parameter_form.cleaned_data
                parameter_id = cd['parameter_id']
                app_name = cd['app_name']
                parameter_name = cd['parameter_name']
                parameter_value = cd['parameter_value']
                
                parameter = ParameterRepo(request=request,app_name=app_name).change_parameter(
                    parameter_id=parameter_id,
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                    )
                if parameter is not None:
                    context['parameter'] = ParameterSerializer(parameter).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
class AddPageLinkApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_link_form = AddPageLinkForm(request.POST)
            if add_page_link_form.is_valid():
                log += 1
                cd=add_page_link_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                url = cd['url']
                
                page_link = PageLinkRepo(request=request).add_page_link(
                    page_id=page_id,
                    title=title,
                    url=url,
                    )
                if page_link is not None:
                    context['page_link'] = PageLinkSerializer(page_link).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
class AddPageDownloadApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddPageDownloadForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                file = request.FILES['file1']
                
                page_download = PageDownloadRepo(request=request).add_page_download(
                    page_id=page_id,
                    title=title,
                    file=file,
                    )
                if page_download is not None:
                    context['page_download'] = PageDownloadSerializer(page_download).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
class AddPageImageApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddPageImageForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                image = request.FILES['image']
                
                page_image = PageImageRepo(request=request).add_page_image(
                    page_id=page_id,
                    title=title,
                    image=image,
                    )
                if page_image is not None:
                    context['page_image'] = PageImageSerializer(page_image).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
class AddPageCommentApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 10
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log = 20
            add_page_comment_form = AddPageCommentForm(request.POST)
            if add_page_comment_form.is_valid():
                log =30
                comment = add_page_comment_form.cleaned_data['comment']
                page_id = add_page_comment_form.cleaned_data['page_id']
                comment=str_to_html(comment)
                page_comment = PageCommentRepo(request=request).add_comment(
                    comment=comment, page_id=page_id)
                if page_comment is not None:
                    log =40
                    context['page_comment'] = PageCommentSerializer(
                        page_comment).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
class DeletePageCommentApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            delete_page_comment_form = DeletePageCommentForm(request.POST)
            if delete_page_comment_form.is_valid():
                log += 1
                page_comment_id = delete_page_comment_form.cleaned_data['page_comment_id']
                done = PageCommentRepo(request=request).delete_comment(
                    page_comment_id=page_comment_id)
                if done:
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)

    
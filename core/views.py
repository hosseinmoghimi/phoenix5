import json
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from utility.calendar import PersianCalendar
from .apps import APP_NAME
from log.repo import LogRepo
from core.enums import ColorEnum, IconsEnum, ParameterNameEnum, PictureNameEnum
from core.models import Download, Link
from core.repo import DownloadRepo, PageDownloadRepo, PageLikeRepo, PageRepo, ParameterRepo, PictureRepo
from .serializers import PageBriefSerializer, PageCommentSerializer, PageImageSerializer, PageDownloadSerializer, PageLinkSerializer
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL, SITE_URL
from django.shortcuts import render
from authentication.repo import ProfileRepo
from core.constants import CURRENCY

from phoenix.server_settings import my_apps
from django.views import View
from .forms import *
# Create your views here.
TEMPLATE_ROOT = "core/"


def CoreContext(request, *args, **kwargs):
    context = {}
    app_name = kwargs['app_name'] if 'app_name' in kwargs else 'core'
    context['APP_NAME'] = app_name
    context['ADMIN_URL'] = ADMIN_URL
    context['STATIC_URL'] = STATIC_URL
    context['MEDIA_URL'] = MEDIA_URL
    context['SITE_URL'] = SITE_URL
    context['apps'] = my_apps

    context['profile'] = ProfileRepo(request=request).me
    parameter_repo = ParameterRepo(request=request, app_name=app_name)

    visitor_counter = parameter_repo.parameter(
        name=ParameterNameEnum.VISITOR_COUNTER, default=1)
    visitor_counter.origin_value = 1+int(visitor_counter.origin_value)
    visitor_counter.save()
    context['visitor_counter'] = visitor_counter.value

    context['CURRENCY'] = CURRENCY
    farsi_font_name = parameter_repo.parameter(
        name=ParameterNameEnum.FARSI_FONT_NAME, default="Vazir").value
    if not farsi_font_name == ParameterNameEnum.FARSI_FONT_NAME and not farsi_font_name == "Default":
        context['farsi_font_name'] = farsi_font_name
    picture_repo = PictureRepo(request=request, app_name=app_name)
    context['app'] = {
        'title': parameter_repo.parameter(name=ParameterNameEnum.TITLE, default=app_name).value,
        'home_url': parameter_repo.parameter(name=ParameterNameEnum.HOME_URL, default="/"+app_name+"/").value,
        'icon': picture_repo.picture(name=PictureNameEnum.FAVICON, default=STATIC_URL+"").image,
        'logo': picture_repo.picture(name=PictureNameEnum.LOGO, default=STATIC_URL+"").image,
    }
    pc = PersianCalendar()
    now = timezone.now()
    current_datetime = pc.from_gregorian(now)
    context['current_date'] = current_datetime[:10]
    context['current_datetime'] = current_datetime
    return context


def PageContext(request, *args, **kwargs):
    profile=ProfileRepo(request=request).me
    context = {}
    if 'page' in kwargs:
        page = kwargs['page']
    if 'page_id' in kwargs:
        page = PageRepo(request=request).page(pk=kwargs['page_id'])
    if page is None:
        raise Http404
    context['page'] = page
    links = page.pagelink_set.all()
    links_s = json.dumps(PageLinkSerializer(links, many=True).data)
    context['links_s'] = links_s
    context['links'] = links

    page_comments = page.pagecomment_set.all()
    context['page_comments'] = page_comments
    context['page_comments_s'] = json.dumps(
        PageCommentSerializer(page_comments, many=True).data)

    related_pages = page.related_pages.all()
    context['related_pages_s'] = json.dumps(
        PageBriefSerializer(related_pages, many=True).data)



    page_likes=PageLikeRepo(request=request).list(page_id=page.id)
    context['page_likes']=page_likes

    if profile is not None:
        my_like = page.my_like(profile_id=profile.id)
        context['my_like'] = my_like
    
    if ProfileRepo(request=request).me is not None:
        context['add_page_comment_form'] = AddPageCommentForm()

    downloads = PageDownloadRepo(request=request).list(page_id=page.id)
    context['downloads'] = downloads
    downloads_s = json.dumps(PageDownloadSerializer(downloads, many=True).data)
    context['page_downloads_s'] = downloads_s
    my_pages_ids = PageRepo(request=request).my_pages_ids()
    if request.user.has_perm(APP_NAME+".add_link") or page.id in my_pages_ids:
        context['add_page_link_form'] = AddPageLinkForm()
    if request.user.has_perm(APP_NAME+".add_download") or page.id in my_pages_ids:
        context['add_page_download_form'] = AddPageDownloadForm()

    if request.user.has_perm(APP_NAME+".add_pageimage") or page.id in my_pages_ids:
        context['add_page_image_form'] = AddPageImageForm()
    if request.user.has_perm(APP_NAME+".change_page") or page.id in my_pages_ids:
        context['add_related_page_form'] = AddRelatedPageForm()
    page_images = page.pageimage_set.all()
    context['images_s'] = json.dumps(
        PageImageSerializer(page_images, many=True).data)

    return context


class DownloadView(View):
    def get(self, request, *args, **kwargs):
        me = ProfileRepo(request=request).me
        download = DownloadRepo(request=request).download(*args, **kwargs)
        if me is None and not download.is_open:
            pass
        elif request.user.has_perm("core.change_download") or download.is_open or me in download.profiles.all():
            if download is None:
                LogRepo(request=request).add_log(
                    title="Http404 core views 2"+str(kwargs), app_name=APP_NAME)
                raise Http404
            return download.download_response()

        # if self.access(request=request,*args, **kwargs) and document is not None:
        #     return document.download_response()
        message_view = MessageView(request=request)
        message_view.links = []
        message_view.links.append(Link(title='تلاش مجدد', color="warning",
                                  icon_material="apartment", url=download.get_download_url()))
        message_view.message_color = 'warning'
        message_view.has_home_link = True
        message_view.header_color = "rose"
        message_view.message_icon = ''
        message_view.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        message_view.message_text = ' شما مجوز دسترسی به این صفحه را ندارید.'
        message_view.header_text = 'دسترسی غیر مجاز'

        return message_view.response()


class MessageView(View):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.links = []
        self.title = None
        self.body = None
        self.message_color = 'warning'
        self.has_home_link = True
        self.header_color = "rose"
        self.message_icon = ''
        self.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        self.message_text = ""
        self.header_text = ""
        self.message_html = ""
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        else:
            self.app_name = 'web'
        if 'title' in kwargs:
            self.title = kwargs['title']
        if 'body' in kwargs:
            self.body = kwargs['body']
        if 'message_html' in kwargs:
            self.message_html = kwargs['message_html']
        if 'message_color' in kwargs:
            self.message_color = kwargs['message_color']
        if 'has_home_link' in kwargs:
            self.has_home_link = kwargs['has_home_link']
        if 'header_color' in kwargs:
            self.header_color = kwargs['header_color']
        if 'message_icon' in kwargs:
            self.message_icon = kwargs['message_icon']
        if 'header_icon' in kwargs:
            self.header_icon = kwargs['header_icon']
        if 'message_text' in kwargs:
            self.message_text = kwargs['message_text']
        if 'header_text' in kwargs:
            self.header_text = kwargs['header_text']

    def show(self, *args, **kwargs):

        return self.response()

    def response(self, *args, **kwargs):
        context = CoreContext(request=self.request, *args, **kwargs)
        if self.header_text is None:
            self.header_text = 'خطا'
        if self.message_text is None:
            self.message_text = 'متاسفانه خطایی رخ داده است.'
        if self.has_home_link:
            btn_home = Link(url=(SITE_URL),
                            color=ColorEnum.PRIMARY+' btn-round',
                            icon_material=IconsEnum.home,
                            title='خانه', new_tab=False)
            self.links.append(btn_home)
        context['links'] = self.links

        context['header_text'] = self.header_text
        context['header_color'] = self.header_color
        context['header_icon'] = self.header_icon

        context['message_color'] = self.message_color
        context['message_icon'] = self.message_icon
        context['message_text'] = self.message_text
        context['message_html'] = self.message_html
        context['body'] = self.body
        context['title'] = self.title

        context['search_form'] = None
        context['no_footer'] = True
        context['no_navbar'] = True
        return render(self.request, TEMPLATE_ROOT+'message.html', context)

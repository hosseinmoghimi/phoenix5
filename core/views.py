from decimal import getcontext
import json
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from utility.calendar import PersianCalendar
from core.apps import APP_NAME
from log.repo import LogRepo
from core.enums import ColorEnum, IconsEnum, ParameterNameEnum, PictureNameEnum
from core.models import Download, Link
from core.repo import DownloadRepo, ImageRepo, PageDownloadRepo, PageImageRepo, PageLikeRepo, PagePermissionRepo, PageRepo, ParameterRepo, PictureRepo, TagRepo
from core.serializers import PagePermissionSerializer,PageBriefSerializer, PageCommentSerializer, PageImageSerializer, PageDownloadSerializer, PageLinkSerializer, PageTagSerializer
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL, SITE_URL
from django.shortcuts import render
from authentication.repo import ProfileRepo
from core.constants import CURRENCY

from phoenix.server_settings import phoenix_apps
from django.views import View
from core.forms import *
# Create your views here.
TEMPLATE_ROOT = "core/"
LAYOUT_PARENT='phoenix/layout.html'


def CoreContext(request, *args, **kwargs):
    context = {}
    context['apps'] = phoenix_apps
    context['LAYOUT_PARENT'] = LAYOUT_PARENT

    installed_apps=[]
    for phoenix_app in phoenix_apps:
        installed_apps.append(phoenix_app['name'])
        context[phoenix_app['name']+'_app_is_installed']=True
    context["installed_apps"]=installed_apps

    app_name = kwargs['app_name'] if 'app_name' in kwargs else 'core'
    context['APP_NAME'] = app_name
    context['ADMIN_URL'] = ADMIN_URL
    context['STATIC_URL'] = STATIC_URL
    context['MEDIA_URL'] = MEDIA_URL
    context['SITE_URL'] = SITE_URL

    profile = ProfileRepo(request=request).me
    context['profile'] = profile
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
        'icon': picture_repo.picture(name=PictureNameEnum.FAVICON, default="").image,
        'logo': picture_repo.picture(name=PictureNameEnum.LOGO, default="").image,
    }
    pc = PersianCalendar()
    now = timezone.now()
    current_datetime = pc.from_gregorian(now)
    context['current_date'] = current_datetime[:10]
    context['current_datetime'] = current_datetime
    from messenger.views import getPusherContext
    context.update(getPusherContext(request=request,profile=profile))


    return context


def PageContext(request, *args, **kwargs):
    if 'page' in kwargs:
        page = kwargs['page']
    if 'page_id' in kwargs:
        page = PageRepo(request=request).page(pk=kwargs['page_id'])
    if page is None:
        raise Http404
    context = {}
    context['page'] = page
    profile=ProfileRepo(request=request).me

    can_read=False
    can_write=False
    
    if profile is not None:
        page_permission=PagePermissionRepo(request=request).list(page_id=page.id,profile_id=profile.id).first()
        if page_permission is not None:
            can_write=page_permission.can_write
        # my_pages_ids=( page_permissions)
        


    can_add_link=False
    can_add_image=False
    can_add_download=False
    can_add_comment=False
    can_add_tag=False
    can_add_location=False
    can_add_related_page=False
    
    if request.user.has_perm(APP_NAME+".view_page"):
        can_read=True
    if can_write or request.user.has_perm(APP_NAME+".change_page"):
        can_read=True
        can_add_link=True
        can_add_image=True
        can_add_download=True
        can_add_comment=True
        can_add_tag=True
        can_add_location=True
        can_add_related_page=True


    
    # links
    if True:
        links = page.pagelink_set.all()
        links_s = json.dumps(PageLinkSerializer(links, many=True).data)
        context['links_s'] = links_s
        context['links'] = links
        if  can_add_link:
            context['add_page_link_form'] = AddPageLinkForm()
    

    # locations
    if True:
        from map.serializers import PageLocationSerializer,LocationSerializer
        from map.repo import LocationRepo,PageLocationRepo
        page_locations =PageLocationRepo(request=request).list(page_id=page.id)
        # context['locations_s'] = json.dumps(LocationSerializer(locations, many=True).data)
        context['page_locations_s'] = json.dumps(PageLocationSerializer(page_locations, many=True).data)
        context['locations_s'] = json.dumps(LocationSerializer([], many=True).data)
        context['all_locations']=LocationRepo(request=request).list()
        if can_add_location :
            from map.forms import AddLocationForm,AddPageLocationForm
            context['add_page_location_form']=AddPageLocationForm()
            context['add_location_form']=AddLocationForm()

    
    # tags
    if True:
        page_tags = page.pagetag_set.all()
        page_tags_s = json.dumps(PageTagSerializer(page_tags, many=True).data)
        context['page_tags_s'] = page_tags_s
        context['page_tags'] = page_tags
        if  can_add_tag:
            context['add_page_tag_form'] = AddPageTagForm()


    # commnets
    if True:
        page_comments = page.pagecomment_set.all()
        context['page_comments'] = page_comments
        context['page_comments_s'] = json.dumps(
            PageCommentSerializer(page_comments, many=True).data)
        if can_add_comment:
            context['add_page_comment_form'] = AddPageCommentForm()


    #permissions
    if True:
        page_permissions=PagePermissionRepo(request=request).list(page_id=page.id)
        context['page_permissions']=page_permissions
        page_permissions_s=json.dumps(PagePermissionSerializer(page_permissions,many=True).data)
        context['page_permissions_s']=page_permissions_s
        if request.user.has_perm(APP_NAME+".change_page"):
            context['add_page_permission_form']=AddPagePermissionForm()
            all_profiles=ProfileRepo(request=request).list()
            context['all_profiles']=all_profiles

    # related_pages
    if True:
        related_pages = page.related_pages.all()
        context['related_pages_s'] = json.dumps(
            PageBriefSerializer(related_pages, many=True).data)
        if can_add_related_page:
            context['add_related_page_form'] = AddRelatedPageForm()



    #keywords
    if True:
        keywords=page.meta_data
        context['keywords'] = keywords


    # downloads
    if True:
        downloads = PageDownloadRepo(request=request).list(page_id=page.id)
        context['downloads'] = downloads
        downloads_s = json.dumps(PageDownloadSerializer(downloads, many=True).data)
        context['page_downloads_s'] = downloads_s
        if can_add_download:
            context['add_page_download_form'] = AddPageDownloadForm()

    #images
    if True:
        page_images = page.pageimage_set.all()
        context['images_s'] = json.dumps(PageImageSerializer(page_images, many=True).data)
        if can_add_image:
            context['add_page_image_form'] = AddPageImageForm()


    # likes
    if True:
        page_likes=PageLikeRepo(request=request).list(page_id=page.id)
        context['page_likes']=page_likes
        if profile is not None:
            my_like = page.my_like(profile_id=profile.id)
            context['my_like'] = my_like

    return context


class DownloadView(View):
    def get(self, request, *args, **kwargs): 
        me = ProfileRepo(request=request).me
        download = DownloadRepo(request=request).download(*args, **kwargs)
        if download is None or (me is None and not download.is_open):
            pass
        elif request.user.has_perm("core.change_download") or download.is_open or me in download.profiles.all():
            file_path = str(download.file.path)
            # return JsonResponse({'download:':str(file_path)})
            import os
            from django.http import HttpResponse
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=' + \
                        os.path.basename(file_path)
                    download.download_counter += 1
                    download.save()
                    return response
                    
        # if self.access(request=request,*args, **kwargs) and document is not None:
        #     return document.download_response()
        message_view = MessageView(request=request)
        message_view.links = []
        message_view.message_color = 'warning'
        message_view.has_home_link = True
        message_view.header_color = "rose"
        message_view.message_icon = ''
        message_view.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        message_view.body = ' شما مجوز دسترسی به این صفحه را ندارید.'
        message_view.title = 'دسترسی غیر مجاز'
        if download is None:
            message_view.body = 'دانلود مورد نظر شما پیدا نشد.'
            message_view.title = 'دانلود مورد نظر پیدا نشد.'
        else:
            message_view.links.append(Link(title='تلاش مجدد', color="warning",
                                  icon_material="apartment", url=download.get_download_url()))

        return message_view.response()
        
         

class PagePermissionsView(View):
    def get(self,request,*args, **kwargs):
        context=CoreContext(request=request)

        profile_id=kwargs['pk']

        page_permissions=PagePermissionRepo(request=request).list(profile_id=profile_id)
        context['page_permissions']=page_permissions
        page_permissions_s=json.dumps(PagePermissionSerializer(page_permissions,many=True).data)
        context['page_permissions_s']=page_permissions_s
        return render(request,TEMPLATE_ROOT+"page-permissions.html",context)
    

class ImageDownloadView(View):
    def get(self, request, *args, **kwargs): 
        image = ImageRepo(request=request).image(*args, **kwargs)
        if image is None:
            raise Http404
        return image.download_response()
 



class TagView(View):
    def get(self, request, *args, **kwargs):
        me = ProfileRepo(request=request).me
        tag = TagRepo(request=request).tag(*args, **kwargs)
        if tag is None:
            raise Http404
        context=CoreContext(request=request,app_name=APP_NAME)
        context['tag']=tag
        page_tags=tag.pagetag_set.all()
        context['page_tags']=page_tags
        return render(request,TEMPLATE_ROOT+"tag.html",context)
        
 
class PageImageView(View):
    def get(self, request, *args, **kwargs):
        me = ProfileRepo(request=request).me
        image = PageImageRepo(request=request).page_image(*args, **kwargs)
        if image is None:
            raise Http404
        context=CoreContext(request=request,app_name=APP_NAME)
        context['image']=image
        context['no_navbar']=True
        context['no_footer']=True
        return render(request,TEMPLATE_ROOT+"image.html",context)
        


class ImageView(View):
    def get(self, request, *args, **kwargs):
        me = ProfileRepo(request=request).me
        image = ImageRepo(request=request).image(*args, **kwargs)
        if image is None:
            raise Http404
        context=CoreContext(request=request,app_name=APP_NAME)
        context['image']=image
        context['no_navbar']=True
        context['no_footer']=True
        return render(request,TEMPLATE_ROOT+"image.html",context)
        
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

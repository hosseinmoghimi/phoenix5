from requests import request
from .models import ContactMessage, Download, Image, Link, Page, PageComment, PageDownload, PageImage, PageLike, PageLink, PagePermission, PageTag, Parameter,Picture, Tag
from .constants import *
from django.db.models import Q
from authentication.repo import ProfileRepo
from .apps import APP_NAME

class ImageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.profile=ProfileRepo(request=self.request).me
        self.objects=Image.objects
    
    def image(self,*args, **kwargs):
        pk=0
        if 'image_id' in kwargs:
            pk=kwargs['image_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        return self.objects.filter(pk=pk).first()

    def list(self,*args, **kwargs):
        objects=self.objects
        return objects


class PageRepo:
    
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Page.objects.all()
    def add_page(self,title,*args, **kwargs):
        new_page=Page(title=title)
        new_page.title=title
        if 'parent_id' in kwargs:
            new_page.parent_id=kwargs['parent_id']
        new_page.save()
        new_page.app_name=new_page.parent.app_name
        new_page.class_name=new_page.parent.class_name
        new_page.save()
        return new_page
    def set_thumbnail_header(self,*args, **kwargs):
        if not self.request.user.has_perm("core.change_page"):
            return
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return

        if 'clear_thumbnail' in kwargs and kwargs['clear_thumbnail']:
            page.thumbnail_origin=None
        else:
            if 'thumbnail' in kwargs:
                thumbnail=kwargs['thumbnail']
                if thumbnail is not None:
                    page.thumbnail_origin=thumbnail
                    page.save()



        if 'clear_header' in kwargs and kwargs['clear_header']:
            page.header_origin=None
        else:
            if 'header' in kwargs:
                header=kwargs['header']
                if header is not None:
                    page.header_origin=header
                    page.save()
        return page

    def add_related_page(self,*args, **kwargs):
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return

        
        page_id=0
        related_page_id=0
        bidirectional=True
        add_or_remove=True
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        if 'related_page_id' in kwargs:
            related_page_id=kwargs['related_page_id']
        if 'bidirectional' in kwargs:
            bidirectional=kwargs['bidirectional']
        if 'add_or_remove' in kwargs:
            add_or_remove=kwargs['add_or_remove']
        if add_or_remove is None:
            add_or_remove=True
        page=self.page(page_id=page_id)
        related_page=self.page(page_id=related_page_id)
        if page is None or related_page is None:
            return None
        if add_or_remove:
            page.related_pages.add(related_page)
            if bidirectional:
                related_page.related_pages.add(page)
            return related_page
        else:
            page.related_pages.remove(related_page)
            if bidirectional:
                related_page.related_pages.remove(page)
            return related_page

    def profile_pages(self,*args, **kwargs):
        my_pages_ids=[]
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        else:
            profile=ProfileRepo(request=self.request).me
            if profile is not None:
                profile_id=profile.id
        my_pages_ids=PagePermissionRepo(request=self.request).list(profile_id=profile_id)
        return Page.objects.filter(id__in=my_pages_ids)
    def toggle_like(self,*args, **kwargs):
        page=self.page(*args, **kwargs)
        profile=ProfileRepo(request=self.request).me
        likes=PageLike.objects.filter(page=page).filter(profile=profile)
        my_like=False
        if len(likes)==0 and profile is not None and page is not None:
            my_like=PageLike(page=page,profile=profile)
            my_like.save()
            my_like=True
        else:
            likes.delete()
        likes_count=page.likes_count()
        return (my_like,likes_count)
    
    def edit_page(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_basicpage"):
            return
        page=self.page(*args, **kwargs)
        if page is None:
            return
        if 'description' in kwargs and kwargs['description']  is not None and not kwargs['description'] == "" :
            page.description=kwargs['description']

        if 'short_description' in kwargs and kwargs['short_description']  is not None and not kwargs['short_description'] == "":
            page.short_description=kwargs['short_description']
        page.save()
        return page


    def edit(self,*args, **kwargs):
        return self.edit_page(*args, **kwargs)




    def page(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

    def list(self,*args, **kwargs):
        objects1=self.objects
        
        if 'app_name' in kwargs:
            objects1 = objects1.filter(Q(app_name=kwargs['app_name']))


        if 'for_home' in kwargs:
            objects1=objects1.filter(for_home=kwargs['for_home'])

            
        if 'search_for' in kwargs:
            ids=[]
            

            objects=objects1.filter(title__contains=kwargs['search_for'])
            for obj in objects:
                ids.append(obj.id)



            page_tags=PageTag.objects.filter(tag__title=kwargs['search_for'])
            for page_tag in page_tags:
                ids.append(page_tag.page.pk)


            objects=objects1.filter(id__in=ids)



        return objects.all()

    
class PageTagRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageTag.objects.all()
        self.profile=ProfileRepo(request=self.request).me
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'tag_id' in kwargs and kwargs['tag_id']>0:
            objects=objects.filter(tag_id=kwargs['tag_id'])
        if 'page_id' in kwargs and kwargs['page_id']>0:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.order_by('-date_added')

    def add_tag(self,*args, **kwargs):
       
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return
        if not 'tag_title' in kwargs:
            return
        tag=Tag.objects.filter(title=kwargs['tag_title']).first()
        if tag is None:
            tag=Tag(title=kwargs['tag_title'])
            tag.save()
        aa=PageTag.objects.filter(page_id=page.id).filter(tag_id=tag.id)
        if len(aa)>0:
            aa.delete()
        else:
            page_tag=PageTag()
            page_tag.tag=tag
            page_tag.page=page
            page_tag.save()
        return PageTag.objects.filter(page_id=page.id)

    def page_tag(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'page_tag_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_tag_id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class PageLikeRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageLike.objects.all()
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            self.app_name=app_name
            self.objects=self.objects.filter(page__app_name=app_name)
        else:
            self.app_name=None
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'profile_id' in kwargs and kwargs['profile_id']>0:
            objects=objects.filter(profile_id=kwargs['profile_id'])
        if 'page_id' in kwargs and kwargs['page_id']>0:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.order_by('-date_added')


class PageCommentRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=PageComment.objects
    def add_comment(self,*args, **kwargs):
        
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return

        profile=ProfileRepo(user=self.user).me
        page_comment=PageComment(comment=kwargs['comment'],page_id=kwargs['page_id'],profile=profile)
        
        page_comment.save()
        return page_comment

    def delete_comment(self,page_comment_id,*args, **kwargs):
        profile=ProfileRepo(user=self.user).me
        page_comment=PageComment.objects.filter(pk=page_comment_id).first()

        if page_comment is not None and page_comment.profile==profile:
            page_comment.delete()
            return True
        return False

    def page_comment(self,*args, **kwargs):
        if 'page_comment_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_comment_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class TagRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.objects=Tag.objects
    

    def tag(self,*args, **kwargs):
        if 'tag_id' in kwargs:
            return self.objects.filter(pk=kwargs['tag_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()


class PictureRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Picture.objects.filter(app_name=self.app_name)
    def list(self,*args, **kwargs):
        return self.objects.filter(app_name=self.app_name)
    def picture(self,*args, **kwargs):
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            self.app_name=app_name
            self.objects=Picture.objects.filter(app_name=app_name)

        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            if name=="":
                return
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None:
                picture=Picture(app_name=self.app_name,name=name)
                picture.app_name=self.app_name
                picture.name=name
                if 'default' in kwargs:
                    picture.image_origin=kwargs['default']
                picture.save()
                return picture
            # (picture,res) = self.objects.get_or_create(name=name,app_name=self.app_name)
            # picture = self.objects.filter(name=name).filter(app_name=self.app_name).first()
            return picture
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(pk=pk).first()
        return picture

    def get(self,*args, **kwargs):
        return self.picture(*args, **kwargs)


class ParameterRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=Parameter.objects.filter(app_name=self.app_name)
        if 'force' in kwargs and kwargs['force']:
            self.objects=Parameter.objects.all()
    
    def change_parameter(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+'.change_parameter'):
            return None
        parameter_id=kwargs['parameter_id'] if 'parameter_id' in kwargs else None
        parameter_name=kwargs['parameter_name'] if 'parameter_name' in kwargs else None
        parameter_value=kwargs['parameter_value'] if 'parameter_value' in kwargs else None
        app_name=self.app_name
        if parameter_id is not None:
            parameter=Parameter.objects.filter(pk=parameter_id).first()
            if parameter is None:
                return None
        elif parameter_name is not None and app_name is not None:
            parameter=Parameter.objects.filter(app_name=app_name).filter(name=parameter_name).first()
            if parameter is None:
                parameter=Parameter(app_name=app_name,name=parameter_name,value_origin="")
                parameter.save()
        
        parameter.origin_value=parameter_value
        parameter.save()
        return parameter

    
    def set(self,*args, **kwargs):
        # if name==ParametersEnum.LOCATION:
        #     value=value.replace('width="600"','width="100%"')
        #     value=value.replace('height="450"','height="400"') 
        value=kwargs['value']
        name=kwargs['name']
        if value is None:
            value=name
        parameter=self.parameter(*args, **kwargs)
        parameter.origin_value=value
        parameter.save()
        return parameter
     
    
    
    def parameter(self,*args, **kwargs):
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)

        parameter=None
        parameter_name=""
        if 'parameter_name' in kwargs:
            parameter_name=kwargs['parameter_name']
        if 'name' in kwargs:
            parameter_name=kwargs['name']
        parameter= self.objects.filter(name=parameter_name).first()
        if parameter is None:
            default=parameter_name
            if 'default' in kwargs:
                default=kwargs['default']
            
            parameter=Parameter(name=parameter_name,app_name=self.app_name,origin_value=default)
            parameter.save()

        if 'id' in kwargs:
            parameter= self.objects.filter(name=kwargs['id']).first()
        if 'parameter_id' in kwargs:
            parameter= self.objects.filter(name=kwargs['parameter_id']).first()
        if 'pk' in kwargs:
            parameter= self.objects.filter(name=kwargs['pk']).first()
            
        return parameter

        

    def list(self,*args, **kwargs):
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)
        objects= self.objects.all()
        return objects


class PageImageRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        self.profile=ProfileRepo(request=self.request).me
        self.objects=PageImage.objects
    def add_page_image(self,title,image,*args, **kwargs):
        
        
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return
        
        # image=Image(title=title,image_main_origin=image)
        # image.save()
        new_page_image=PageImage(image_main_origin=image,page_id=page.id,title=title)
        
        new_page_image.save()
        return new_page_image
    def delete_page_image(self,image_id,page_id,*args, **kwargs):
        if self.user.has_perm(APP_NAME+".delete_pageimage"):
                
            pi=PageImage.objects.filter(image_id=image_id).filter(page_id=page_id)
            if len(pi)>0:
                pi.delete()
                if 'delete_image' in kwargs and kwargs['delete_image']:
                    Image.objects.filter(pk=image_id).delete()

                return True
  

    def page_image(self,*args, **kwargs):
        pk=0
        if 'page_image_id' in kwargs:
            pk=kwargs['page_image_id']
        elif 'image_id' in kwargs:
            pk=kwargs['image_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        return self.objects.filter(pk=pk).first()


class PageDownloadRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=PageDownload.objects.all()
     
    def add_page_download(self,title,file,priority=1000,*args, **kwargs):
        
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return

        if page.app_name=='web':
            is_open=True
        else:
            is_open=False

        page_download=PageDownload(icon_fa="fa fa-download",title=title,is_open=is_open,file=file,priority=priority,page=page,profile=self.profile)
        page_download.save()
        page_download.profiles.add(self.profile)
        return page_download

    
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects


class PagePermissionRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=PagePermission.objects
        if self.user.has_perm(APP_NAME+".view_pagepermission"):
            # self.objects=self.objects
            pass
        elif self.profile is not None:
            self.objects=self.objects.filter(profile_id=self.profile.id)
        else:
            self.objects=PagePermission.objects.filter(pk=0)
    def my_pages_ids(self):
        my_pages_ids=[]
        if self.profile is not None:
            page_permissions=PagePermissionRepo(request=self.request).list()
            # my_pages_ids=( page_permissions)
            for page_permission in page_permissions:
                my_pages_ids.append(page_permission.page.id)
        return my_pages_ids
     
    def add_page_permission(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_pagepermission"):
            return
        # page=PageRepo(request=self.request).page(*args, **kwargs)
        # profile=ProfileRepo(request=self.request).profile(*args, **kwargs)
        # if page is None or profile is None:
        #     return
        PagePermission.objects.filter(page_id=kwargs['page_id']).filter(profile_id=kwargs['profile_id']).delete()
        page_permission=PagePermission()
        page_permission.page_id=kwargs['page_id']
        page_permission.profile_id=kwargs['profile_id']
        page_permission.can_write=kwargs['can_write']

        page_permission.save()
        return page_permission
         
    def page_permission(self,*args, **kwargs):
        if 'page_permission_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_permission_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()


    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'profile_id' in kwargs:
            objects=objects.filter(profile_id=kwargs['profile_id'])
        return objects.all()


class PageLinkRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=PageLink.objects.all()
     
    
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    def add_page_link(self,title,url,*args, **kwargs):
        
       
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_page"):
            can_write=True
        if not can_write:
            self.profile=ProfileRepo(request=self.request).me
            if self.profile is not None:
                page_permission=PagePermission.objects.filter(page_id=page.id).filter(profile_id=self.profile.id).first()
                if page_permission is not None:
                    can_write=page_permission.can_write
        if page is None or not can_write:
            return


        new_page_link=PageLink(title=title,page_id=page.id,url=url,icon_fa="fa fa-link",profile=self.profile)
        new_page_link.new_tab=True
        new_page_link.save()
        return new_page_link




class LinkRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=Link.objects.all()
     
    
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects
    

class ContactMessageRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.app_name=""
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        self.objects = ContactMessage.objects.filter(app_name=self.app_name)
        self.me=ProfileRepo(user=self.user).me
    def list(self):
        objects=self.objects
        return objects

    def add(self,*args, **kwargs):
        contact_message=ContactMessage()
        contact_message.app_name=self.app_name
        if 'full_name' in kwargs:
            contact_message.full_name=kwargs['full_name']
        if 'subject' in kwargs:
            contact_message.subject=kwargs['subject']
        if 'email' in kwargs:
            contact_message.email=kwargs['email']
        if 'message' in kwargs:
            contact_message.message=kwargs['message']
        if 'mobile' in kwargs:
            contact_message.mobile=kwargs['mobile']
        contact_message.save()
        return contact_message

        
class DownloadRepo:
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        
        self.objects=Download.objects.all()
     
    def download(self,*args, **kwargs):
        if 'download_id' in kwargs:
            return self.objects.filter(pk=kwargs['download_id']).first()
        if 'page_download_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_download_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()

         
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects

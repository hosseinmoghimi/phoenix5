
from . import views,apis
from .apps import APP_NAME
from django.urls import path

app_name=APP_NAME
urlpatterns = [
    path('',views.HomeView.as_view(),name="home"),
    path('search/',views.SearchView.as_view(),name="search"),
    path('settings/',views.SettingsView.as_view(),name="settings"),
    path('backup/',views.BackupView.as_view(),name="backup"),
    path('page/<int:pk>/',views.PageView.as_view(),name="page"),
    path('page_downloads/',views.PageDownloadsView.as_view(),name="page_downloads"),
    path('page_links/',views.PageLinksView.as_view(),name="page_links"),
    path('pages_permissions/<int:pk>/',views.PagePermissionsView.as_view(),name="pages_permissions"),
    path('change_parameter/',apis.ChangeParameterApi.as_view(),name="change_parameter"),
    path('add_page_link/',apis.AddPageLinkApi.as_view(),name="add_page_link"),
    path("download/<int:pk>/",views.DownloadView.as_view(),name='download'),
    path("tag/<int:pk>/",views.TagView.as_view(),name='tag'),
    path("pagetag/<int:pk>/",views.PageTagView.as_view(),name='pagetag'),
    path("image/<int:pk>/",views.ImageView.as_view(),name='image'),
    path("page_print/<int:pk>/",views.PagePrintView.as_view(),name='page_print'),
    path("page_show/<int:pk>/",views.PageShowView.as_view(),name='page_show'),
    path("page_edit/<int:pk>/",views.PageEditView.as_view(),name='page_edit'),
    path("image_download/<int:pk>/",views.ImageDownloadView.as_view(),name='image_download'),
    path("pageimage/<int:pk>/",views.PageImageView.as_view(),name='pageimage'),

    
    path('download_media/',views.DownloadMediaApi.as_view(),name="download_media"),
    path('download_uploads/',views.DownloadUploadsApi.as_view(),name="download_uploads"),
  
  
    path('add_page_download/',apis.AddPageDownloadApi.as_view(),name="add_page_download"),
    path('add_page_image/',apis.AddPageImageApi.as_view(),name="add_page_image"),

    path('encrypt/',apis.EncryptApi.as_view(),name="encrypt"),
    path('decrypt/',apis.DecryptApi.as_view(),name="decrypt"),
    path('delete_page_comment/',apis.DeletePageCommentApi.as_view(),name="delete_page_comment"),
    path('add_page_comment/',apis.AddPageCommentApi.as_view(),name="add_page_comment"),
    path('add_contact_message/',apis.AddContactMessageApi.as_view(),name="add_contact_message"),
    path('add_related_page/',apis.AddRelatedPageApi.as_view(),name="add_related_page"),
    path('toggle_like/',apis.TogglePageLikeApi.as_view(),name="toggle_like"),
    path('add_page_tag/',apis.AddPageTagApi.as_view(),name="add_page_tag"),

    path('add_page_permission/',apis.AddPagePermissionApi.as_view(),name="add_page_permission"),
    path('set_thumbnail_header/',apis.SetThumbnailHeaderApi.as_view(),name="set_thumbnail_header"),
    path('delete_page_image/',apis.DeletePageImageApi.as_view(),name="delete_page_image"),

]

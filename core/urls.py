
from . import views,apis
from .apps import APP_NAME
from django.urls import path

app_name=APP_NAME
urlpatterns = [


    path('change_parameter/',apis.ChangeParameterApi.as_view(),name="change_parameter"),
    path('add_page_link/',apis.AddPageLinkApi.as_view(),name="add_page_link"),
    path("download/<int:pk>/",views.DownloadView.as_view(),name='download'),
    path("tag/<int:pk>/",views.TagView.as_view(),name='tag'),
    path("image/<int:pk>/",views.ImageView.as_view(),name='image'),
    path("image_download/<int:pk>/",views.ImageDownloadView.as_view(),name='image_download'),
    path("pageimage/<int:pk>/",views.PageImageView.as_view(),name='pageimage'),
    path('add_page_download/',apis.AddPageDownloadApi.as_view(),name="add_page_download"),
    path('add_page_image/',apis.AddPageImageApi.as_view(),name="add_page_image"),

    path('delete_page_comment/',apis.DeletePageCommentApi.as_view(),name="delete_page_comment"),
    path('add_page_comment/',apis.AddPageCommentApi.as_view(),name="add_page_comment"),
    path('add_contact_message/',apis.AddContactMessageApi.as_view(),name="add_contact_message"),
    path('add_related_page/',apis.AddRelatedPageApi.as_view(),name="add_related_page"),
    path('toggle_like/',apis.TogglePageLikeApi.as_view(),name="toggle_like"),
    path('add_page_tag/',apis.AddPageTagApi.as_view(),name="add_page_tag"),

]

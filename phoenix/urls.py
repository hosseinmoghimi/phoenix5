
from django.contrib import admin
from django.urls import path,include,re_path

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT, DEBUG,QRCODE_ROOT
from django.views.static import serve

from web3auth import urls as web3auth_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('core/', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('market/', include('market.urls')),
    path('web/', include('web.urls')),
    # path('entity/', include('entity.urls')),
    path('pm/', include('projectmanager.urls')),
    path('accounting/', include('accounting.urls')),
    path('transport/', include('transport.urls')),
    path('map/', include('map.urls')),
    path('stock/', include('stock.urls')),
    path('log/', include('log.urls')),
    path('archive/', include('archive.urls')),
    path('messenger/', include('messenger.urls')),
    path('', include('accounting.urls')),
    path('wallet/', include('wallet.urls')),
    re_path(r'^', include(web3auth_urls)),
# web3auth_urls
    re_path(r'^qrcode/(?P<path>.*)$', serve, {'document_root': QRCODE_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]

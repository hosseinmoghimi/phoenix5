
from django.contrib import admin
from django.urls import path,include,re_path

from phoenix.server_settings import PUBLIC_ROOT

from .settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT, DEBUG,QRCODE_ROOT
from django.views.static import serve
from authentication.views import LogoutViews,LoginViews
# from core.icon import FavIconView
# from web3auth import urls as web3auth_urls
from core.views import HomeView
urlpatterns = [
    path('', HomeView.as_view(),name="home"),
    path('login/', LoginViews.as_view(),name="login"),
    path('logout/', LogoutViews.as_view(),name="logout"),
    path('admin/', admin.site.urls),
    path('accounting/', include('accounting.urls')),
    path('authentication/', include('authentication.urls')),
    path('library/', include('library.urls')),
    path('core/', include('core.urls')),
    path('realestate/', include('realestate.urls')),
    path('health/', include('health.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('market/', include('market.urls')),
    path('pm/', include('projectmanager.urls')),
    path('utility/', include('utility.urls')),
    path('web/', include('web.urls')),
    path('contact/', include('contact.urls')),
    path('transport/', include('transport.urls')),
    path('polls/', include('polls.urls')),
    path('map/', include('map.urls')),
    path('stock/', include('stock.urls')),
    path('guarantee/', include('guarantee.urls')),
    path('mafia/', include('mafia.urls')),
    path('log/', include('log.urls')),
    path('archive/', include('archive.urls')),
    path('organization/', include('organization.urls')),
    path('resume/', include('resume.urls')),
    path('scheduler/', include('scheduler.urls')),
    path('messenger/', include('messenger.urls')),
    path('chef/', include('chef.urls')),
    path('bms/', include('bms.urls')),
    path('wallet/', include('wallet.urls')),
    path('warehouse/', include('warehouse.urls')),
    path('school/', include('school.urls')),
    path('loyaltyclub/', include('loyaltyclub.urls')),
    
    # path('favicon.ico', FaviconView.as_view(),name="favicon"),
    # re_path(r'^', include(web3auth_urls)),
# web3auth_urls
    
    re_path(r'^qrcode/(?P<path>.*)$', serve, {'document_root': QRCODE_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': PUBLIC_ROOT}),
]

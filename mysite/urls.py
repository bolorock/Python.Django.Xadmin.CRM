# coding=utf-8
from django.conf.urls.defaults import *
import xadmin
from xadmin.plugins import xversion
from mysite.main import registe_menus
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from crm.views import get_product, get_computingTax

# admin.autodiscover()
xadmin.autodiscover()

xversion.registe_models()

registe_menus() #注册菜单


# urlpatterns = patterns('',
#     (r'^admin/', include(admin.site.urls)),
#     (r'^admin/doc/', include('django.contrib.admindocs.urls')),
#     ('^index/$', index),
#     ('^time/$', current_datetime),
#     (r'^time/plus/(\d{1,2})/$', hours_ahead),
# )

urlpatterns = patterns('',
    url(r'xadmin/', include(xadmin.site.urls)),
    url('^crm/getProduct/$', get_product),
    url('^crm/get_computingTax/$',get_computingTax),
)

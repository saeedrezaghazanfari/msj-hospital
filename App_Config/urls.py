from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from . import views


urlpatterns = [
    path('', views.select_lang_redirect),
]

urlpatterns += i18n_patterns(
    
    # Custom Views
    path('404', views.page_not_found_view),
    path('403', views.page_forbidden_view),
    path('500', views.page_server_error_view),

    # APP
    path('', include('hospital_auth.urls', namespace='auth')),
    path('', include('hospital_setting.urls', namespace='setting')),
    path('', include('hospital_blog.urls', namespace='blog')),
    path('', include('hospital_news.urls', namespace='news')),
    path('', include('hospital_contact.urls', namespace='contact')),
    path('', include('hospital_website.urls', namespace='website')),

    # PACKAGES
    path('change/language/', views.activate_language, name='activate_lang'),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "App_Config.views.page_not_found_view"
handler403 = "App_Config.views.page_forbidden_view"
handler500 = "App_Config.views.page_server_error_view"

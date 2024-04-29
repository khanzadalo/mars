from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
import orders_app.views

urlpatterns = [
    path('orders_app/', include('orders_app.urls')),
    path('admin/', admin.site.urls),
    path('', orders_app.views.mainpage, name='mainpage'),
    path('devices/', orders_app.views.get_devices, name='get_devices'),
    path('devpage/', orders_app.views.devpage, name='devpage')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "djangoapp"
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    # path for about view
    path("about/", views.about, name="about"),
    # path for contact us view
    path("contact/", views.contact, name="contact"),
    # path for registration
    path("register/", views.register, name="register"),

    # path for login
    # path('login/',views.login,name='sign_up'),
    # path for logout
    path("logout/", views.logout_view, name="logout"),
    path(route="macroapp/", view=views.macroapp, name="macroapp"),

    # path for dealer reviews view
    # path for add a review view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^find/$', views.WholeScrapping.as_view()),
    url(r'^find/(?P<pagina>\w+)/$', views.IndividualScrapping.as_view()),
]
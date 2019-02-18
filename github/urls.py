from django.conf.urls import url, include
from github import views as views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="login.html")),
    url(r'^api/social_login/$', views.SocialLoginView.as_view(), name='login'),
    url(r'^api/user_detail/$', views.GetUserDetailView.as_view(), name='home'),
    url(r'^oauth/', include('social_django.urls', namespace='social'))
]

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import requests
User = get_user_model()

# Create your views here.


class SocialLoginView(APIView):
    def get(self, request):
        # response = redirect('api/user_detail/')
        # return response
        user = request.user
        github_login = user.social_auth.get(provider='github')
        params = {'access_token': github_login.access_token}
        data = requests.get("https://api.github.com/user",
                            params=params).json()
        try:
            user = User.objects.get(username=data['login'])
        except ObjectDoesNotExist:
            User.objects.create(
                github_user_id=data['id'],
                prf_picture_url=data['avatar_url'],
                username=data['login']
            )
        else:
            if user.github_user_id == '':
                user.github_user_id = data['id']
                user.prf_picture_url = data['avatar_url']
                user.save()
        return HttpResponseRedirect('/api/user_detail/')


class GetUserDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home.html'

    def get(self, request):
        user = request.user
        user_id = user.social_auth.get(provider='github').uid
        try:
            user1 = User.objects.get(github_user_id=user_id)
        except ObjectDoesNotExist:
            return Response({"data": "error"})
        data = {
            "username": user1.username,
            "avatar_url": user1.prf_picture_url
        }
        return Response({"data": data})

import allauth.socialaccount.models
import dj_rest_auth.utils
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from .serializers import CrewSerializer, UserSerializer
from CrewManager.models import Crew, User

from json.decoder import JSONDecodeError
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from django.conf import settings
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import redirect
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User
from CrewManager.models import Crew

# Create your views here.

class CrewViewSet(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

crew_list = CrewViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

crew_detail = CrewViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

class Kakao_Login(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        kakao_access_code = request.GET.get('code', None)
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {kakao_access_code}",
            "Content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        kakao_response = requests.post(url, headers=headers)
        if not kakao_response.ok:
            return HttpResponseBadRequest(content=kakao_response)
        kakao_response = json.loads(kakao_response.text)
        #return JsonResponse(kakao_response)
        if User.objects.filter(email=kakao_response['kakao_account']['email']).exists():
            user = User.objects.get(email=kakao_response['kakao_account']['email'])
            accesstoken, refreshtoken = dj_rest_auth.utils.jwt_encode(user)

            info = {"access_token":f"{accesstoken}",
                    "refresh_token":f"{refreshtoken}",
                    "user": {
                        "pk": user.id,
                        "email": user.email
                    },
                    "status" : "exist"
                    }


            return JsonResponse(info)
        else:
            User(
                email=kakao_response['kakao_account']['email'],
                profile_image=kakao_response['kakao_account']['profile']['profile_image_url']
            ).save()
            user = User.objects.get(email=kakao_response['kakao_account']['email'])
            accesstoken, refreshtoken = dj_rest_auth.utils.jwt_encode(user)

            info = {"access_token": f"{accesstoken}",
                    "refresh_token": f"{refreshtoken}",
                    "user": {
                        "pk": user.id,
                        "email": user.email
                    },
                    "status": "new"
                    }

            return JsonResponse(info)
        # else:
        #
        #
        #     User(
        #         uid=kakao_response['id'],
        #         platform="1",
        #         user_email=kakao_response['kakao_account'].get('email', None),
        #         name=kakao_response['properties']['nickname'],
        #
        #     ).save()
        #     user = User.objects.get(uid=kakao_response['id'])
        #     jwt_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)
        #     return HttpResponse(f'id:{user.id}, name:{user.name}, token:{jwt_token}, exist:false')
        return JsonResponse(kakao_response)



@api_view(['POST'])
def crew_join(request,pk):
    if request.method == 'POST':
        userid = request.POST['userid']
        if not User.objects.filter(id=userid).exists():
            return Response({'error':'user'+userid+' is not in DB'})
        else:
            c = Crew.objects.get(id=pk)
            if c.members.filter(id=userid).exists():
                if userid == c.manager.id:
                    return Response({'failed':'크루장은 탈퇴할 수 없습니다.'})
                c.members.remove(userid)
                return Response({'success':'정상적으로 크루에 탈퇴하였습니다.'})
            else:
                u = User.objects.get(id=userid)
                if c.members.count() >= c.member_limit:
                    return Response({'failed':'크루 등록인원이 최대치에 도달하여 등록할 수 없습니다.'})
                if str(u.community) in c.community_limit:
                    c.members.add(userid)
                    return Response({'success':'정상적으로 크루에 등록했습니다.'})

                else:
                    return Response({'failed': '크루 공동체 정책에 의해서 등록할 수 없습니다.'})
        return Response({'error':"test"})




# KAKAO_CALLBACK_URI = 'http://127.0.0.1:8000/apis/accounts/kakao/login/callback/'
# BASE_URL = 'http://127.0.0.1:8000/apis/'
# def kakao_login(request):
#     kakao = allauth.socialaccount.models.SocialApp.objects.filter(name='kakao').all()
#     rest_api_key = str(kakao[0].client_id)
#     # rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
#     )
# def kakao_callback(request):
#     kakao = allauth.socialaccount.models.SocialApp.objects.filter(name='kakao').all()
#     rest_api_key = str(kakao[0].client_id)
#     secretkey = str(kakao[0].secret)
#     code = request.GET.get("code")
#     redirect_uri = KAKAO_CALLBACK_URI
#     """
#     Access Token Request
#     """
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}&client_secret={secretkey}")
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get("access_token")
#     """
#     Email Request
#     """
#     profile_request = requests.get(
#         "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
#     profile_json = profile_request.json()
#     kakao_account = profile_json.get('kakao_account')
#     """
#     kakao_account에서 이메일 외에
#     카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
#     print(kakao_account) 참고
#     """
#     # print(kakao_account)
#     email = kakao_account.get('email')
#     """
#     Signup or Signin Request
#     """
#     try:
#         user = User.objects.get(email=email)
#         # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#         if social_user.provider != 'kakao':
#             return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
#         # 기존에 Google로 가입된 유저
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#     except User.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {'access_token': access_token, 'code': code}
#         accept = requests.post(
#             f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#         # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
#         accept_json = accept.json()
#         accept_json.pop('user', None)
#         return JsonResponse(accept_json)
#
# class KakaoLogin(SocialLoginView):
#     adapter_class = kakao_view.KakaoOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = KAKAO_CALLBACK_URI
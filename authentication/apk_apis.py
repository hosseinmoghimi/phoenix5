
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.repo import ProfileRepo
from authentication.serializers import ProfileSerializer
from django.http import JsonResponse
from core.constants import SUCCEED,FAILED
from.apps import APP_NAME
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class CustomAuthToken(ObtainAuthToken):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        result=FAILED
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user'] 
        cleaned_data=request.POST
        (request,profile,token,created)=ProfileRepo(request=request).authenticate_for_apk(username=cleaned_data['username'],password=cleaned_data['password'])
            

        profile_s=ProfileSerializer(profile).data
        context={
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'created':created,
            'profile':profile_s,
            'result':result,
        }
        ProfileRepo(request=request).logout()
        return Response(context)

        
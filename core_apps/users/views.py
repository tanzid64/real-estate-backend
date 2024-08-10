from django.shortcuts import render
import logging
from typing import Optional, Any
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Create your views here.

logger = logging.getLogger(__name__)

def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str]=None) -> None:
  access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
  cookie_settings = {
    "path": settings.COOKE_PATH, 
    "secure": settings.COOKE_SECURE, 
    "httponly": settings.COOKE_HTTPONLY,
    "samesite": settings.COOKE_SAMESITE,
    "max_age": access_token_lifetime
  }
  response.set_cookie("access", access_token, **cookie_settings)
  if refresh_token:
    refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
    refresh_cookie_settings = cookie_settings.copy()
    refresh_cookie_settings["max_age"] = refresh_token_lifetime
    response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

  logged_in_cookie_settings = cookie_settings.copy()
  logged_in_cookie_settings["httponly"] = False
  response.set_cookie("logged_in", "true", **logged_in_cookie_settings)

class CustomTokenObtainPairView(TokenObtainPairView):
  def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    token_res = super().post(request, *args, **kwargs)
    if token_res.status_code == status.HTTP_200_OK:
      access_token = token_res.data['access']
      refresh_token = token_res.data['refresh']

      if access_token and refresh_token:
        set_auth_cookies(token_res, access_token, refresh_token)
        token_res.data.pop('access', None)
        token_res.data.pop('refresh', None)
        token_res.data["message"] = "Login Successful"
      else:
        token_res.data["message"] = "Login Failed"
        logger.error("Access token or refresh token not found")

    return token_res
  
class CustomTokenRefreshView(TokenRefreshView):
  def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    refresh_token = request.COOKIES.get("refresh")
    refresh_res = super().post(request, *args, **kwargs)
    if refresh_token:
      request.data["refresh"] = refresh_token

    if refresh_res.status_code == status.HTTP_200_OK:
      access_token = refresh_res.data['access']
      refresh_token = refresh_res.data['refresh']

      if access_token and refresh_token:
        set_auth_cookies(refresh_res, access_token, refresh_token)
        refresh_res.data.pop('access', None)
        refresh_res.data.pop('refresh', None)
        refresh_res.data["message"] = "Access Token refreshed successfully"
      else:
        refresh_res.data["message"] = "Refresh Failed"
        logger.error("Access token or refresh token not found")

    return refresh_res

class CustomProviderAuthView(ProviderAuthView):
  def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    provider_res = super().post(request, *args, **kwargs)
    if provider_res.status_code == status.HTTP_201_CREATED:
      access_token = provider_res.data['access']
      refresh_token = provider_res.data['refresh']

      if access_token and refresh_token:
        set_auth_cookies(provider_res, access_token, refresh_token)
        provider_res.data.pop('access', None)
        provider_res.data.pop('refresh', None)
        provider_res.data["message"] = "Login Successful"
      else:
        provider_res.data["message"] = "Access or refresh token not found in provider response"
        logger.error("Access or refresh token not found in provider response")

    return provider_res
  
class LogoutAPIView(APIView):
  def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    response.delete_cookie("logged_in")
    return response
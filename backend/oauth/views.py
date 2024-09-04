from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
import requests

client_id = settings.CLIENT_ID
client_secret = settings.CLIENT_SECRET
redirect_uri = "http://localhost:8000/oauth/login/redirect"

def login(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"message": "Hello, World!"})

def login42(request: HttpRequest):
    return redirect(
        f"https://api.intra.42.fr/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )

def login42_redirect(request: HttpRequest):
    code = request.GET.get("code")
    # print(f"code: {code}")
    user = exchange_code_for_token(code)

    return JsonResponse({"user": user}) # for test
    return 

def exchange_code_for_token(code: str) -> str:
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post("https://api.intra.42.fr/oauth/token", data=data)
    # print(f"response: {response.json()}")

    # test start (using token) 
    access_token = response.json()["access_token"]
    # print(f"access_token: {access_token}")
    response = requests.get("https://api.intra.42.fr/v2/me", headers={"Authorization": f"Bearer {access_token}"})
    user = response.json()
    return user
    # test end
    return response

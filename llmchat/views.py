from django.shortcuts import render

# Create your views here.

# views.py
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home_page(request):
    return render(request, 'home_page.html')


@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        user_message = json.loads(request.body).get("message", "")
        headers = {
            "Authorization": "Bearer VOTRE_CLE_OPENROUTER",
            "Content-Type": "application/json",
        }
        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": user_message}],
        }
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        answer = response.json()["choices"][0]["message"]["content"]
        return JsonResponse({"response": answer})

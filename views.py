from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import json
from .models import ChatMessage

def chat_view(request):
    csrf_token = get_token(request)  
    return render(request, "chat/chat.html", {"csrf_token": csrf_token})

def get_messages(request):
    messages = list(ChatMessage.objects.values("name", "message", "timestamp"))
    return JsonResponse({"messages": messages})

def save_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")
        ChatMessage.objects.create(name=name, message=message)
        return JsonResponse({"status": "Message saved!"})
@csrf_exempt 
def send_message(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name", "Anonymous")
            message = data.get("message", "")

            if message.strip():
                ChatMessage.objects.create(name=name, message=message)
                return JsonResponse({"status": "success", "message": "Message sent!"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

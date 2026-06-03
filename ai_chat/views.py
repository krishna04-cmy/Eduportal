from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from groq import Groq
from .models import ChatMessage
import json
from decouple import config

client = Groq(api_key=config("GROQ_API_KEY"))  # ← Apni Groq API key yahan paste karo

@login_required(login_url='/login/')
def ai_chat_view(request):
    # messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')[:20]
    messages = []
    return render(request, 'ai_chat/ai_chat.html', {
        'messages': messages,
    })

@login_required(login_url='/login/')
def ai_chat_send(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        # Groq API call
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful educational assistant for EduPortal school. Help students with their studies, answer questions about subjects, and provide guidance."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500,
        )

        ai_response = completion.choices[0].message.content

        # Save to database
        ChatMessage.objects.create(
            user=request.user,
            message=user_message,
            response=ai_response,
        )

        return JsonResponse({'response': ai_response})

    return JsonResponse({'error': 'Invalid request'}, status=400)
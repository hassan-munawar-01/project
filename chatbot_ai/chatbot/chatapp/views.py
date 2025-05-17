from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot_logic import SmartChatBot
import re
import traceback

bot = SmartChatBot()

def index(request):
    return render(request, 'index.html')

def clean_bot_response(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"###\s*", r"\n\n", text)
    text = re.sub(r"^\s*[-*]\s*", "• ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s*", "• ", text, flags=re.MULTILINE)
    return text.strip()



@csrf_exempt
def get_response(request):
    user_input = request.GET.get('user_input')
    lang = request.GET.get('lang', 'en')

    if not user_input:
        return JsonResponse({'response': 'Please enter a message.'})

    try:
        response = bot.get_response(user_input, lang)
        clean_response = clean_bot_response(response)
        return JsonResponse({'response': clean_response})
    except Exception as e:
        print("🔥 ERROR:", e)
        traceback.print_exc()  # will show detailed error in console
        return JsonResponse({'response': f'Error occurred: {str(e)}'})

def home(request):
    return render(request, "home.html")
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm
from .models import User, CallCount


@login_required
def chat(request):
    context = {}
    return render(request, "chatbot_tutorial/chatbot.html", context)


def respond_to_websockets(message):
    jokes = {
        "stupid": [
            """Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
            """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association.""",
        ],
        "fat": [
            """Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
            """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """,
        ],
        "dumb": [
            """Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
            """Yo' Mama is so dumb, she locked her keys inside her motorcycle.""",
        ],
    }

    result_message = {"type": "text"}
    if "fat" in message["text"]:
        result_message["text"] = random.choice(jokes["fat"])

    elif "stupid" in message["text"]:
        result_message["text"] = random.choice(jokes["stupid"])

    elif "dumb" in message["text"]:
        result_message["text"] = random.choice(jokes["dumb"])

    elif message["text"] in ["hi", "hey", "hello"]:
        result_message[
            "text"
        ] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message[
            "text"
        ] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message


def register_view(request):
    if request.user.is_authenticated():
        return redirect('chat')

    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                CallCount.objects.create(user=user)
                messages.add_message(
                    request, messages.INFO, "Registered. Log in to continue."
                )
                return redirect('login')
            else:
                messages.add_message(
                    request, messages.INFO, "User with username already exists."
                )

    context = {"form": form}
    return render(request, "chatbot_tutorial/register.html", context)


def login_view(request):
    if request.user.is_authenticated():
        return redirect('chat')

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("chat")
            else:
                messages.add_message(request, messages.INFO, "Invalid credentials.")

    context = {"form": form}

    return render(request, "chatbot_tutorial/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')


def call_count_view(request):
    data = []
    for u in User.objects.all().iterator():
        data.append(
            {
                'user': u.username,
                'stupid': u.count.stupid,
                'fat': u.count.fat,
                'dumb': u.count.dumb,
                'query': u.count.query
            }
        )

    context = {
        'data': data,
        'user': True if request.user.is_authenticated() else False
    }

    return render(request, "chatbot_tutorial/call_count.html", context)

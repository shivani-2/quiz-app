from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import *
import random

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to some page after login
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    context = {'categories' : Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    
    return render(request, 'home.html', context)

def quiz(request):
    context = {'category' : request.GET.get('category')}
    return render(request, 'quiz.html', context)

def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        
        if request.GET.get('category'):
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))
            #__ works as a dot to link, and icontains is a method in Django to check

        question_objs=list(question_objs)
        data = []
        random.shuffle(question_objs)
        for q_obj in question_objs:
            data.append({
                "uid": q_obj.uid,
                "category": q_obj.category.category_name,
                "question": q_obj.question,
                "description": q_obj.description,
                "marks": q_obj.marks,
                "answers": q_obj.get_answers(),
                #answer:question_answer.answer,  
                #try same with relational object
            })

        payload = {'status':True, 'data': data}

        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong")
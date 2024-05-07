from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import *
import random

# Create your views here.

def home(request):
    #return HttpResponse("Hello from Django")
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
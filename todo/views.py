from django . shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email =  request.POST.get('email')
        password = request.POST.get('password')
        print(username, email, password)

        my_user = User.objects.create_user(username, email, password)
        my_user.save()
        return redirect('/login')

    return render(request, 'signup.html')


def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('/todo')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')

    return render(request,'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('task')
        obj = models.TODOO(title=title, user=request.user)
        obj.save()
        res = models.TODOO.objects.filter(user = request.user).order_by('-date')
        return redirect('/todo')
    res = models.TODOO.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})

@login_required(login_url='/login')
def edit_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno)  # Fetch task or return 404 if not found

    if request.method == 'POST':
        title = request.POST.get('title')  # Ensure your form uses name="title"
        obj.title = title
        obj.save()
        return redirect('/todo')  # Redirect without passing context

    return render(request, 'edit_todo.html', {'obj': obj}) 

@login_required(login_url='/login')
def delete_todo(request, srno):
    obj = get_object_or_404(TODOO, srno=srno)
    obj.delete()
    return redirect('/todo')


def signout(request):
    logout(request)
    return redirect('/login')
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

#login 
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
                login(request, user)
                return redirect('/super_admin/')
        elif user is not None and user.is_registrar_admin:
                login(request, user)
                return redirect('/registrar_admin/')
        elif user is not None and user.is_registrar_staff:
                login(request, user)
                return redirect('/graduates/')
        else:
            messages.info( request,'username or password is incorrect')
    return render(request, 'accounts/login.html')

#logout
def logout_page(request):
    logout(request)
    return redirect('accounts:login')


def not_found(request):
    return render(request, 'accounts/404.html')


def me(request):
    return render(request, 'accounts/me.html')





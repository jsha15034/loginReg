from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
# print(bcrypt.hashpw)
# print(bcrypt.checkpw)

# Create your views here.


#render
def index(request):
    return render(request, 'login_reg/index.html')

def main(request):
    # print(request.session['user_id'])
    if not 'user_id' in request.session:
        return redirect('/')
    return render(request,'login_reg/main.html')







#redirect
def register(request):
    #print(request.POST)

    #VALIDATIONS FIRST!
    error = False
    if len(request.POST['first_name']) < 2:
        messages.error(request, 'your name sucks')
        error = True
    if len(request.POST['last_name']) < 2:
        messages.error(request, 'your last name sucks')
        error = True
    if len(request.POST['email']) < 2:
        messages.error(request, 'your email sucks')
        error = True
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request, 'Passwords not matching')
        error = True

    matching_users = User.objects.filter(email = request.POST['email'])
    if len(matching_users) > 0:
        messages.error(request, 'Email taken')
        error = True
    
    if error:
        return redirect('/')
    #VALIDATIONS END

    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed) 

    # print(user)
    request.session['user_id'] = user.id
    # print(request.session['user_id'])
    return redirect('/main')


def login(request):
    #print(request.POST)
    matching_users = User.objects.filter(email = request.POST['email'])
    if len(matching_users) > 0:
        #email matched, now check pw
        user = matching_users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/main')
        else:
            print('bad password')
    else:
        print('no matching email')
    return redirect ('/')

def logout(request):
    request.session.clear()
    return redirect('/')
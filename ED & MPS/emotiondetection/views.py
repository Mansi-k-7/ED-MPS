from django.shortcuts import render
from django.contrib import messages
from user.models import *

def index(request):
    return render(request, 'index.html')

def Home(request):
    return render(request, 'index.html')

def commonlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        if email =='admin' and password =='admin' or email == 'Admin' and password == 'Admin':
            registered_users = userregistermodel.objects.all()
            data = userimagepredictionmodel.objects.all()
            return render(request, 'admin/adminhome.html', {'registered_users': registered_users, 'data':data})
        else:
            try:
                user = userregistermodel.objects.get(email=email, password=password)
                if user.status == 'activated':
                    request.session['email'] = user.email
                    data = userimagepredictionmodel.objects.filter(email=email)
                    return render(request, 'user/userhome.html', {'data':data})
                else:
                    messages.error(request, 'User not activated')
                    return render(request, 'index.html')
            except userregistermodel.DoesNotExist:
                messages.error(request, 'Invalid credentials')
                return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    
def adminhome(request):
    registered_users = userregistermodel.objects.all()
    data = userimagepredictionmodel.objects.all()
    return render(request, 'admin/adminhome.html', {'registered_users': registered_users, 'data':data})

def AdminActiveUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        userregistermodel.objects.filter(id=id).update(status=status)
        registered_users = userregistermodel.objects.all()
        data = userimagepredictionmodel.objects.all()
        return render(request, 'admin/adminhome.html', {'registered_users': registered_users, 'data':data})

def adminlogout(request):
    return render(request, 'index.html')

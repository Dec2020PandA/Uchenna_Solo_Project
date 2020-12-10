import random
from .models import User
from django.shortcuts import render,redirect
from django.contrib import messages
from time import gmtime, strftime

def index(request):
    if 'user_id' not in request.session:
        return redirect('/display_login')

            
    if 'activities' not in request.session:
        request.session['activities'] = []

    if 'coins' not in request.session:
        request.session['coins']= int(20)
    
    if request.session['coins']==0:
        return redirect("/no_more_coins")
    
    
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
    "user":user
}
    return render(request, "index.html",context)

# Create your views here.
def process_money(request):
    if request.method == 'GET':
        return redirect('/')   
        
    if request.method == 'POST':
        
        user = User.objects.get(id=request.session["user_id"])
        time=strftime("%Y-%m-%d %H:%M %p", gmtime())

            

        if 'farm' in request.POST:
            request.session['coins']-= int(1)
            gift=random.randint(10, 30)
            user.account_balance += gift
            user.save()
            
            request.session['activities'].append("You just gained {} from the farm: ({})".format(gift,time))

            
        elif 'cave' in request.POST:
            request.session['coins']-= int(1)
            var_num=random.randint(20, 50)
            
            if (random.randint(1, 5)!=1):
                user.account_balance += var_num
                user.save()
                request.session['activities'].append("You just gained {} from the cave: ({})".format(var_num,time))
            else:
                
                user.account_balance -= var_num
                user.save()
                request.session['activities'].append("You just lost {} from the cave: ({})".format(var_num_half,time))
     
            
        elif 'house' in request.POST:
            request.session['coins']-= int(1)
            var_num = random.randint(50,80)
            var_num_half = random.randint(25,40)
            if (random.randint(1, 2)==1):
                user.account_balance +=  var_num
                user.save()
                request.session['activities'].append("You just gained {} from the house: ({})".format(var_num,time))
            else:
                
                user.account_balance -=  var_num_half
                user.save()
                request.session['activities'].append("You just lost {} from the house: ({})".format(var_num_half,time)) 
            
                   
        elif 'casino' in request.POST:
            request.session['coins']-= int(1)
            var_num = random.randint(80, 150)
            var_num_half = random.randint(40,75)
            
            if (random.randint(1, 5)==1):
                    user.account_balance += var_num
                    user.save()
                    request.session['activities'].append("You just gained {} from the casino: ({})".format(var_num,time))         
            else:       
                 
                user.account_balance -= var_num_half
                user.save()
                request.session['activities'].append("You just lost {} from the casino: ({})".format(var_num_half,time))

        if request.session['coins']==0:
            return redirect("/no_more_coins")
        else:
            return redirect("/")    

def no_more_coins(request):
    
    return render(request, "no_more_coins.html")  
    

def add_coins(request):
    if request.method == 'GET':
        return redirect('/')   
        
    if request.method == 'POST':
        request.session['coins']+= int(request.POST['coins_to_add'])
        return redirect('/')

def reset(request):
    request.session.flush()
    return redirect("/")

def display_login(request):
    return render(request,"login.html")

def display_register(request):
    return render(request,"register.html")

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    
    return redirect('/')


def register(request):
    if request.method == "GET":
        return redirect('/display_register')
    errors = User.objects.register_validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/display_register')
    else:
        
        new_user = User.objects.register(request.POST)
             
        return redirect('/')

def multiply(request):
    pass

def display_invest(request):
    return render(request,"invest.html")

def invest(request):
    if request.method == "GET":
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    if user.account_balance < 1:
        messages.error(request, 'You cannot invest with a deficit account')
        return redirect('/display_invest')

    
     
    user.account_balance -= int(request.POST['amount'])
    user.invested_balance += int(request.POST['amount'])
    user.save()
    return redirect('/')

def withdraw(request):
    if request.method == "GET":
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    
    if user.invested_balance < int(request.POST['amount']):
        messages.error(request, 'You cannot withdraw more than you have')
        return redirect('/display_invest')
    
    user.invested_balance -= int(request.POST['amount'])
    user.account_balance += int(request.POST['amount'])
    user.save()
    return redirect('/')
    
    
    



def logout(request):
    request.session.clear()
    return redirect('/login')
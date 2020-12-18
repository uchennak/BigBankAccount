import random
from .models import User
from django.shortcuts import render,redirect
from django.contrib import messages
from time import gmtime, strftime

def index(request):
    if 'user_id' not in request.session:
        return redirect('/display_login')
    
    user = User.objects.get(id=request.session['user_id'])

    context = {
    "user":user
}
    
    if 'activities' not in request.session:
        request.session['activities'] = []
    
    if user.coins == 0:
        return redirect("/no_more_coins")
    
    return render(request, "index.html",context)

# Create your views here.
def process_money(request):
    if request.method == 'GET':
        return redirect('/')   
        
    if request.method == 'POST':
        
        user = User.objects.get(id=request.session["user_id"])
        time=strftime("%Y-%m-%d %H:%M %p", gmtime())

            
        if 'farm' in request.POST:
            
            user.coins -= int(1)
            gift=random.randint(10, 30)
            user.account_balance += gift
            user.save()
            
            request.session['activities'].append("You just gained {} from the farm: ({})".format(gift,time))
            request.session.save()
            
           

        elif 'cave' in request.POST:
            user.coins -= int(1)
            user.save()
            var_num=random.randint(20, 50)
            
            if (random.randint(1, 5)!=1):
                user.account_balance += var_num
                user.save()
                request.session['activities'].append("You just gained {} from the cave: ({})".format(var_num,time))
                request.session.save()
            else:
                var_num_half = var_num
                user.account_balance -= var_num
                user.save()
                request.session['activities'].append("You just lost {} from the cave: ({})".format(var_num,time))
                request.session.save()
     
            
        elif 'house' in request.POST:
            user.coins -= int(1)
            user.save()
            var_num = random.randint(50,80)
            var_num_half = random.randint(25,40)
            if (random.randint(1, 2)==1):
                user.account_balance +=  var_num
                user.save()
                request.session['activities'].append("You just gained {} from the house: ({})".format(var_num,time))
                request.session.save()
            else:
                
                user.account_balance -=  var_num_half
                user.save()
                request.session['activities'].append("You just lost {} from the house: ({})".format(var_num_half,time)) 
                request.session.save()
            
                   
        elif 'casino' in request.POST:
            user.coins -= int(1)
            user.save()
            var_num = random.randint(80, 150)
            var_num_half = random.randint(40,75)
            
            if (random.randint(1, 5)==1):
                    user.account_balance += var_num
                    user.save()
                    request.session['activities'].append("You just gained {} from the casino: ({})".format(var_num,time)) 
                    request.session.save()        
            else:       
                 
                user.account_balance -= var_num_half
                user.save()
                request.session['activities'].append("You just lost {} from the casino: ({})".format(var_num_half,time))
                request.session.save()

        if user.coins==0:
            return redirect("/no_more_coins")
        else:
            return redirect("/")    


def no_more_coins(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
    "user":user
}
    
    return render(request, "no_more_coins.html",context)  
    

def add_coins(request):
    if request.method == 'GET':
        return redirect('/')   
        
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        if user.coin_click_counter != 1:
            user.coin_click_counter -= 1
            user.save()
        else:
            user.coin_click_counter = 5
            user.coins += 5
            user.save()
            return redirect('/')

        

        return redirect('/no_more_coins')

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

def increase_investment(request):
    
    user = User.objects.get(id=request.session['user_id'])
    
    if user.invested_balance <1:
        messages.error(request, "You don't have anything in your account")
        return redirect('/display_invest')

    if user.investment_click_counter != 1:
        user.investment_click_counter -= 1
        user.save()
    else:
        user.investment_click_counter = 5
        
        add_to_investment = int(user.invested_balance / 10)
        user.invested_balance += add_to_investment
        user.save()
        messages.error(request, "Added "+str(add_to_investment)+" to your invested account")
    return redirect('/display_invest') 



def display_invest(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
    "user":user
}
    return render(request,"invest.html",context)

def invest(request):
    if request.method == "GET":
        return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    if user.account_balance < 100:
        messages.error(request, 'You need at least 100 in your account to invest ')
        return redirect('/display_invest')

    if int(request.POST['amount']) > user.account_balance:
        messages.error(request, "You can't invest more than you have")
        return redirect('/display_invest')

    if int(request.POST['amount']) < 100:
        messages.error(request, 'The minimum amount to deposit is 100')
        return redirect('/display_invest')

    
     
    user.account_balance -= int(request.POST['amount'])
    user.invested_balance += int(request.POST['amount'])
    user.save()
    return redirect('/display_invest')

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
    return redirect('/display_invest')
    
    
def display_account(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
    "user":user
}
    return render(request,"display_account.html",context)


def logout(request):
    request.session.clear()
    return redirect('/login')
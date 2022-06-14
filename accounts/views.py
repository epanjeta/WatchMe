from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from cart.models import Cart

def visitorIpAddress(request):

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def badPassword(firstName, lastName, username, password):
    if password != None and firstName.lower() in password.lower():
        return True
    if password != None and lastName.lower() in password.lower():
        return True
    if password != None and username.lower() in password.lower():
        return True
    return False

def commonPassword(password):
    file = open('accounts/commonpasswords.txt', 'r')
    common_values = [line.rstrip("\n") for line in file]
    if any(value == password for value in common_values):
        return True
    return False

def userHasCart(user1):
    cart = Cart.objects.filter(user = user1, isActive = True)
    if cart.count() == 0:
        return False
    else:
        return True

# Create your views here.

def register_view(request):
    if request.method == 'POST':
    # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        username = email.split("@")[0]

        if User.objects.filter(email=email).exists():
            messages.error(request, 'That email is being used!')

        if len(first_name) == 0:
            messages.error(request, 'First name is required!')

        if len(last_name) == 0:
            messages.error(request, 'Last name is required!')

        if len(password) < 8:
            messages.error(request, 'Password must have at least 8 characters!')

        if password != password2:
            messages.error(request, 'Passwords do not match')

        if badPassword(first_name, last_name, username, password):
            messages.error(request, 'Password can not containt first name, last name or email')

        if commonPassword(password):
            messages.error(request, 'This is a common password, please change it')

        poruke = get_messages(request)
        if len(poruke) != 0:
            return redirect('register')
        
        else:
          # Looks good
          user = User.objects.create_user(username=username, password=password,email=email,first_name=first_name,last_name=last_name)
          # Login after register
          # auth.login(request, user)
          # messages.success(request, 'You are now logged in')
          # return redirect('index')
          user.save()
          cart = Cart.create(user)
          cart.save()
          messages.success(request, 'You are now registered and can log in')
          return redirect('login')
    else:
        return render(request, 'accounts/register.html')

def login_view(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    username = email.split("@")[0]

    user = auth.authenticate(username=username, password=password, request=request)

    if user is not None:
      auth.login(request, user)
      if not userHasCart(user):
          cart = Cart.create(user)
          cart.save()
      return redirect('home')
    else:
      messages.error(request, 'Invalid credentials')
      return redirect('login')
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('home')

def lockout(request, credentials, *args, **kwargs):
    return render(request, 'accounts/lockout.html')

def myProfile_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        context = {'user': current_user}
        return render(request, 'accounts/myprofile.html', context)
    else:
        context = {'message': 'Please log in so you can access your personal information'}
        return render(request, 'pages/permission_denied.html', context)

def editProfile_view(request):
    if request.method == 'POST':

        current_user = request.user
        userDb = User.objects.get(username=current_user.username)

        first_name = request.POST.get('first_name', current_user.first_name)
        last_name = request.POST.get('last_name', current_user.last_name)
        email = request.POST.get('email', current_user.email)

        print(first_name, last_name, email)

        if current_user.email != email:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used!')
                return redirect('edit_profile')
        
        username = email.split("@")[0]
        userDb.first_name = first_name
        userDb.last_name = last_name
        userDb.email = email
        userDb.username = username
        userDb.save()

        return redirect('profile')

    else:
        current_user = request.user
        if current_user.is_authenticated:
            context = {'user': current_user}
            return render(request, 'accounts/edit_profile.html', context)
        else:
            context = {'message': 'Please log in so you can access your personal information'}
            return render(request, 'pages/permission_denied.html', context)
    
def editProfilePassword_view(request):
    if request.method == 'POST':
        current_user = request.user
        userDb = User.objects.get(username=current_user.username)

        newPassword1 = request.POST.get('newpassword1', None)
        newPassword2 = request.POST.get('newpassword2', None)
        oldPassword = request.POST.get('oldpassword', None)

        if oldPassword is not None and oldPassword:
            if userDb.check_password(oldPassword):
                if newPassword1 is not None and newPassword2 is not None and newPassword1 == newPassword2:
                    if len(newPassword1) < 8:
                        messages.error(request, 'Password must have at least 8 characters!')
                    if commonPassword(newPassword1):
                        messages.error(request, 'This is a common password, please change it')
                    if badPassword(current_user.first_name, current_user.last_name, current_user.username, newPassword1):
                        messages.error(request, 'Password can not containt first name, last name or email')
                else:
                    messages.error(request, 'Passwords do not match')
            else:
                messages.error(request, 'Old password is not correct')
        else:
            messages.error(request, 'Please enter your old password')

        poruke = get_messages(request)
        if len(poruke) != 0:
            return redirect('edit_password')

        else:
            userDb.set_password(newPassword1)
            userDb.save()
            messages.success(request, 'Password changed successfully, please log back in')
            return redirect('login')

    else:
        current_user = request.user
        if current_user.is_authenticated:
            context = {'user': current_user}
            return render(request, 'accounts/edit_password.html', context)
        else:
            context = {'message': 'Please log in so you can access your personal information'}
            return render(request, 'pages/permission_denied.html', context)

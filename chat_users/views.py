from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile

# Create your views here.


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, username=None):
        return render(request, 'chat_users/profile.html')
    




class CreateUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'chat_users/signup.html')
    
    def post(self, request):
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.warning(request, "username already exists, enter another username")
        if User.objects.filter(email = email).exists():
            messages.warning(request, "email already exists, enter another username")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully")
        
        return redirect('signin')
    

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, username=None):
        
        # There is no need to send data from backend to frontend form because user data is already available in session  
        # user = request.user
        # print("This users first_name",user.email)   

        return render(request, 'chat_users/edit_profile.html')
    
    def post(self, request):
        user_obj = request.user
        profile_obj = user_obj.userprofile

        user_obj.username = request.POST.get('username')
        user_obj.first_name = request.POST.get('first_name')
        user_obj.last_name = request.POST.get('last_name')
        user_obj.email = request.POST.get('email')
        user_obj.save()

        profile_obj.user_phone_no = request.POST.get('user_phone_no')
        profile_obj.bio = request.POST.get('bio')
        profile_obj.profile_image = request.FILES.get('profile_image')
        profile_obj.save()


        print("--------",profile_obj.bio)

        messages.success(request, "Your profile is updated")

        return redirect('profile')


class LoginUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'chat_users/login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid username")
            return redirect('signin')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Invalid credential")
            return redirect('signin')
        
        login(request, user)

        # print('User logged in', user)

        return redirect('home')




class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        # print("This is logout view")
        logout(request)
        return redirect('signin')
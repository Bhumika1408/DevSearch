from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .models import Profile,Skill
from django.urls import conf
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from .utils import searchProfiles,paginateProfiles

# Create your views here.


def loginUser(request):
    page='login'
    print(page)
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')

            
        
    return render(request,'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request,'User was loged out')
    return redirect('login')


def registerUser(request):
    page='register'
    form=CustomUserCreationForm()
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            messages.success(request,"User accoutn was created!!")

            login(request,user)
            return redirect('edit-account')
        else:
            print(form.errors)
            messages.error(request,"An error has occured during registration")


    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles,search_query=searchProfiles(request)

    custom_range,profiles=paginateProfiles(request,profiles,3)

    context={'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    topSkills=profile.skill_set.exclude(description__exact="")
    otherSkills=profile.skill_set.filter(description="")
    context={'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.user_profile
    print("u is:",vars(request.user.user_profile))

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.user_profile
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid:
            form.save()

            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url="login")
def createSkill(request):
    profile=request.user.user_profile
    form=SkillForm()

    if request.method=='POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            form.as_p()
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill was added successfully')
            return redirect('account')
        

    context={'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url="login")
def updateSkill(request,pk):
    profile=request.user.user_profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)

    if request.method=='POST':
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill was updated successfully')
            return redirect('account')
        

    context={'form':form}
    return render(request,'users/skill_form.html',context)


def deleteSkill(request,pk):
    profile=request.user.user_profile
    skill=profile.skill_set.get(id=pk)
    print(skill)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context={'object':skill}
    print(context)
    return render(request,'delete_template.html',context)
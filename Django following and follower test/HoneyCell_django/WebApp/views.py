from django.shortcuts import render

# allow us to redirect
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.template import RequestContext, loader

# import the User class in models.py
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# import the auth.models User
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from WebApp.models import *


@login_required
def index(request):
    print("in the index function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/index.html', context)



# registration is normal route, and login is login is "django.contrib.views.login"
def registration(request):
    errors = []
    context = {}
    if request.method == "GET":
        return render(request, 'WebApp/register.html', context)

    # add 'errors' attribute to the context
    context['errors'] = errors

    password1 = request.POST['password']
    password2 = request.POST['password_confirmation']

    if password1 != password2:

        print("Passwords did not match.")

        # error1 happens
        errors.append("Passwords did not match.")

    if len(User.objects.all().filter(username = request.POST['user_name'])) > 0:
        print("Username is already taken.")

        # error2 happens
        errors.append("Username is already taken.")

    if errors:
        return render(request, 'WebApp/register.html', context)

    # create a new user from the valid form data, using create_user function with 2 arguments, 'username' and 'password'
    new_user = User.objects.create_user(username=request.POST['user_name'], password=request.POST['password'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
    new_user.save()

    # using 'authenticate' function
    new_user = authenticate(username = request.POST['user_name'], password = request.POST['password'])

    # using 'login' function
    login(request, new_user)

    # using 'redirect' function
    return redirect(reverse('message'))

@login_required
def message(request):
    print("in the message function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/message.html', context)

@login_required
def upload(request):
    print("in the upload function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/upload.html', context)

@login_required
def preprocess(request):
    print("in the preprocess function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/preprocessing.html', context)

@login_required
def visualization(request):
    print("in the visualization function.")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/knnresult.html', context)

# def logout view
def my_logout(request):
    logout(request)
    return redirect(reverse('index'))

@login_required
def honeycell(request):
    print("in the honeycell function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/honeycell.html', context)

@login_required
def honeycomb(request):
    print("in the honeycomb function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/honeycomb.html', context)

@login_required
def analytics(request):
    print("in the analytics function")
    context = {}
    user = request.user
    context['user'] = user
    return render(request, 'WebApp/analytics.html', context)


@login_required
def show_users(request):
    print("in the show_users function.")

    context = {}
    context['current_user'] = request.user


    users_followship = []
    context['users_followship'] = users_followship

    print("%" * 30)
    print()
    print("%" * 30)

    for each_user in User.objects.all():
        if each_user != request.user:
            if len(Followship.objects.filter(following=request.user, follower=each_user)):

                each_user_followship = {}
                users_followship.append(each_user_followship)

                each_user_followship['user'] = each_user
                each_user_followship['is_followed'] = True
            else:
                each_user_followship = {}
                users_followship.append(each_user_followship)

                each_user_followship['user'] = each_user
                each_user_followship['is_followed'] = False

    return render(request, 'WebApp/show_users.html', context)


@login_required
def follow(request, user_id):
    print("in the follow function.")

    print("*" * 30)

    print(request)
    print(user_id)

    context = {}
    context['current_user'] = request.user

    selected_user = User.objects.get(id=user_id)

    new_followship_instance = Followship(following=request.user,
                                         follower=selected_user)
    new_followship_instance.save()
    print("Already save new_followship_instance.")

    return HttpResponseRedirect(reverse("show_users"))


@login_required
def del_follow(request, user_id):
    print("in the unfollow function.")

    print(request)
    print(user_id)

    context = {}
    context['current_user'] = request.user

    selected_user = User.objects.get(id=user_id)

    followship = Followship.objects.get(following=request.user,
                                        follower=selected_user)
    followship.delete()
    print("The Followship object already delete.")

    return HttpResponseRedirect(reverse("show_users"))


    return HttpResponseRedirect(reverse("show_users"))


@login_required
def show_followships(request):
    print("in the function show_followships.")

    context = {}
    context['current_user'] = request.user

    followships = Followship.objects.all()
    context['followships'] = followships

    return render(request, 'WebApp/show_followships.html', context)
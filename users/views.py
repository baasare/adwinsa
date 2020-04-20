from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, QueryForm


# Create your views here.

def index(request):
    if request.method == 'GET':
        form = QueryForm()
    else:
        form = QueryForm(request.POST)
        if form.is_valid():
            query = form.save(commit=False)
            query.save()
        else:
            args = {'form': form}
            return render(request, 'users/index.html', args)

    args = {'form': form}

    return render(request, "users/index.html", args)


@login_required
def user_list(request):
    users = get_user_model().objects.all()
    return render(request, 'users/user_list.html', {'users': users})


@login_required
def user_detail(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    patients = user.patients.all()
    return render(request, 'users/user_detail.html', {'user': user, 'patients': patients})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email_verified = True
            user.save()
            return redirect('index')
        else:
            args = {'form': form}
            return render(request, 'users/signup.html', args)
    else:
        form = CustomUserCreationForm()

    args = {'form': form}
    return render(request, 'users/signup.html', args)


def user_login(request):
    if request.method == 'POST':
        next_page = request.POST.get('next')
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in")
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request=request,
                  template_name="users/signin.html",
                  context={"form": form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")

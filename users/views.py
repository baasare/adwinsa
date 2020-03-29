from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import CustomUserCreationForm, ContactForm
from .tokens import token_generator


# Create your views here.

def token_email(user, current_site, path, email_subject, template_name, to_email, from_email):
    message = render_to_string(template_name=template_name, context={
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': token_generator.make_token(user),
        'path': path
    }).strip()
    email = EmailMessage(subject=email_subject, body=message, to=[to_email], from_email=from_email, )
    email.send()


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully, login via the app or website')
    else:
        return HttpResponse('Activation link is invalid!')


def index(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data.get('from_email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            try:
                email = EmailMessage(subject=subject, body=message, to=["interactivelearning2020@gmail.com"],
                                     from_email=from_email, )
                email.send()
                messages.success(request, "Success! Thank you for your message")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            args = {'form': form}
            return render(request, 'users/index.html', args)

    return render(request, "users/index.html", {'form': form})


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
            user.is_active = False
            user.email_verified = False
            user.save()

            current_site = get_current_site(request)
            path = 'activate'
            email_subject = 'Activate Your Account'
            template_name = 'users/activate_account.html'
            to_email = form.cleaned_data.get('email')
            from_email = "Adwinsa <noreply@adwinsa.com>"
            token_email(user, current_site, path, email_subject, template_name, to_email, from_email)

            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
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
                # if form.cleaned_data.get('remember_me'):
                #     request.session.set_expiry(1209600)  # 2 weeks
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

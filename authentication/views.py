from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm  
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

# Login view
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
        else:
            print("formerrors:",form.errors)
            messages.error(request, "Invalid email or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {"form": form})

# Signup view
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/signup.html', {"form": form})

# Logout view
def user_logout(request):
    print("Logout view triggered")  
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after the password change
            messages.success(request, "Your password has been successfully updated!")
            return redirect("home")  # Redirect to the home page or any other page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "authentication/change_password.html", {"form": form})


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            try:
                send_mail(
                    subject=f"Contact Us Message from {name}",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],  # Admin email
                    fail_silently=False,
                )
                messages.success(request, "Thank you for contacting us! We will get back to you shortly.")
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, "An error occurred while sending your message. Please try again.")
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'authentication/contact_us.html')

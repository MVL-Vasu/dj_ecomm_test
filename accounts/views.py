from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import UserProfile

# clerk
# import os
# from django.http import JsonResponse
# from clerk_backend_api import Clerk
# from jose import jwt

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('products:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


# CLERK_JWT_ISSUER = "https://grand-impala-47.clerk.accounts.dev"  # check in Clerk dashboard
# CLERK_JWT_AUDIENCE = "pk_test_Z3JhbmQtaW1wYWxhLTQ3LmNsZXJrLmFjY291bnRzLmRldiQ"  # also from dashboard
# CLERK_JWT_KEY = os.getenv("CLERK_JWT_VERIFICATION_KEY")  # copy from dashboard

# clerk
# def protected(request):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header:
#         return JsonResponse({"error": "No token"}, status=401)

#     token = auth_header.split(" ")[1]
#     clerk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))
#     print(clerk)

#     try:
#         payload = jwt.decode(
#             token,
#             CLERK_JWT_KEY,
#             algorithms=["RS256"],
#             audience=CLERK_JWT_AUDIENCE,
#             issuer=CLERK_JWT_ISSUER,
#         )
#         return JsonResponse({"message": "Hello!", "user_id": payload["sub"]})
#     except Exception as e:
#         print("Exception => " , e)
#         return JsonResponse({"error": "Invalid token"}, status=401)


from django.urls import path

from users.views import JWTLoginAPIView, SignupAPIView, UserDetailAPIView

app_name = "users"

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', JWTLoginAPIView.as_view(), name='login'),
    path('me/', UserDetailAPIView.as_view(), name='user-detail'),
]

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class SignupAPIView(APIView):
  """API view to register a new user.

  Allows unauthenticated access.
  """

  permission_classes = [AllowAny]

  @extend_schema(
      request=UserRegistrationSerializer,
      responses={201: UserSerializer},
      tags=['Authentication'],
  )
  def post(self, request):
    """Handle POST request for user registration.

    Args:
      request: HTTP request.

    Returns:
      HTTP response with created user data.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user_data = UserSerializer(user).data
    return Response(
        {'message': 'User registered successfully.', 'user': user_data},
        status=status.HTTP_201_CREATED,
    )


class JWTLoginAPIView(APIView):
  """Authenticate user and return JWT access and refresh tokens.

  Allows unauthenticated access.
  """

  permission_classes = [AllowAny]

  @extend_schema(
      request=UserLoginSerializer,
      responses={200: UserSerializer},
      tags=['Authentication'],
  )
  def post(self, request):
    """Handle POST request to authenticate user.

    Args:
      request: HTTP request.

    Returns:
      HTTP response with JWT tokens and user data.
    """
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        },
        status=status.HTTP_200_OK,
    )


class UserDetailAPIView(APIView):
  """Return authenticated user details.

  Requires JWT authentication.
  """

  permission_classes = [IsAuthenticated]

  @extend_schema(
      responses={200: UserSerializer},
      tags=['Authentication'],
  )
  def get(self, request):
    """Handle GET request for user details.

    Args:
      request: HTTP request.

    Returns:
      HTTP response with user details.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


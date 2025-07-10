from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
  """Serializer for registering a new user.

  Validates that passwords match and conform to password policies.

  Example:
    {
      "email": "john@example.com",
      "name": "John Doe",
      "dob": "1990-01-01",
      "password": "StrongPass123",
      "password2": "StrongPass123"
    }
  """

  password = serializers.CharField(
      write_only=True, required=True, style={'input_type': 'password'})
  password2 = serializers.CharField(
      write_only=True, required=True, label='Confirm Password', style={'input_type': 'password'})

  class Meta:
    model = User
    fields = ['id', 'name', 'email', 'dob', 'password', 'password2']

  def validate(self, data):
    """Check passwords match and validate password strength.

    Args:
      data: Incoming serializer data.

    Returns:
      Validated data dictionary.

    Raises:
      serializers.ValidationError: If passwords do not match or fail validation.
    """
    if data['password'] != data['password2']:
      raise serializers.ValidationError({
          'password2': 'Password confirmation does not match password.'
      })

    validate_password(data['password'])
    return data

  def create(self, validated_data):
    """Create a user with encrypted password.

    Args:
      validated_data: Validated input data.

    Returns:
      Created user instance.
    """
    validated_data.pop('password2')
    user = User.objects.create_user(
        email=validated_data['email'],
        name=validated_data.get('name', ''),
        dob=validated_data.get('dob'),
        password=validated_data['password']
    )
    return user


class UserLoginSerializer(serializers.Serializer):
  """Serializer for user login input validation.

  Example:
    {
      "email": "john@example.com",
      "password": "StrongPass123"
    }
  """

  email = serializers.EmailField(required=True)
  password = serializers.CharField(
      required=True, style={'input_type': 'password'}, write_only=True)

  def validate(self, data):
    """Validate email and password and authenticate user.

    Args:
      data: Incoming serializer data.

    Returns:
      Dictionary containing authenticated 'user'.

    Raises:
      serializers.ValidationError: If credentials are invalid.
    """
    from django.contrib.auth import authenticate

    user = authenticate(
        email=data.get('email'),
        password=data.get('password')
    )
    if user is None:
      raise serializers.ValidationError('Invalid email or password.')
    if not user.is_active:
      raise serializers.ValidationError('User account is disabled.')

    return {'user': user}


class UserSerializer(serializers.ModelSerializer):
  """Serializer for returning user details.

  Example:
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john@example.com",
      "dob": "1990-01-01",
      "created_at": "2024-01-01T00:00:00Z",
      "modified_at": "2024-01-01T00:00:00Z"
    }
  """

  class Meta:
    model = User
    fields = ['id', 'name', 'email', 'dob', 'created_at', 'modified_at']
    read_only_fields = ['id', 'created_at', 'modified_at']

from django.contrib import admin

# Register your models here.

"""Admin configuration for CustomUser model."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
  """Admin interface for CustomUser model."""

  list_display = ('email', 'name', 'dob', 'is_active', 'is_staff', 'created_at')
  list_filter = ('is_active', 'is_staff', 'created_at')
  search_fields = ('email', 'name')
  ordering = ('email',)
  readonly_fields = ('created_at', 'modified_at')

  fieldsets = (
      (None, {'fields': ('email', 'password')}),
      ('Personal Info', {'fields': ('name', 'dob')}),
      ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
      ('Important dates', {'fields': ('last_login', 'created_at', 'modified_at')}),
  )

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'dob', 'password1', 'password2'),
      }),
  )

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class Role(models.Model):
    role_name = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=40)

    def __str__(self):
        return self.display_name

class UserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, department, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        if not username:
            raise ValueError("The Username field must be set.")

        from .models import Role
        student_role, _ = Role.objects.get_or_create(
            role_name="STUDENT", defaults={"display_name": "Student"}
        )
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, department=department, role=student_role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, department, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        from .models import Role
        admin_role, _ = Role.objects.get_or_create(role_name="ADMIN", defaults={"display_name": "Admin"})
        extra_fields["role"] = admin_role

        return self.create_user(email, username, first_name, last_name, department, password, **extra_fields)



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users", null=True, blank=True)
    department = models.CharField(max_length=100)

    REQUIRED_FIELDS = ["username", "first_name", "last_name", "department"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
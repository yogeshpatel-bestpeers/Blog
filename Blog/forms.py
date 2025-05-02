import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Blog, Category, Comment, CustomUser


class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not re.search(r"^(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$", password):
            raise ValidationError(
                "Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character (e.g., !@#$%^&*)."
            )
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ["category", "title", "featured_image", "content"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your comment..."}
            )
        }

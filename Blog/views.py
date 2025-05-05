from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView

from .forms import BlogForm, CategoryForm, CommentForm, LoginForm, SignupForm
from .models import Blog, Category, Comment, CustomUser, Like
from .utils import (
    blog_page,
    category_url,
    generate_password_reset_link,
    home_url,
    login_url,
    userprofile_url,
)


class Custom_password_reset_request(TemplateView):
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            reset_link = generate_password_reset_link(user, request)
            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "Password Reset    link Send..")
            return render(request, self.template_name)
        except User.DoesNotExist:
            messages.error(request, "Account not found.. ")
            return render(request, self.template_name)


def custom_password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    token_generator = PasswordResetTokenGenerator()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            user.set_password(password)
            user.save()
            messages.success(request, "sucessfully password reset")
            return render(request, "password_reset_complete.html")
        return render(
            request,
            "Blog/UserAuth/password_reset_form.html",
            {"validlink": True},
        )
    else:
        return render(
            request,
            "Blog/UserAuth/password_reset_form.html",
            {"validlink": False},
        )


# Create your Views here.
class Index(TemplateView):
    def get(self, request):
        return redirect(home_url)


class UserSigup(TemplateView):
    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):

        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return redirect(login_url)

        return render(request, self.template_name, {"form": form})


class UserLogin(TemplateView):

    def get(self, request):
        if request.user and request.user.is_authenticated:
            return redirect(home_url)
        else:
            form = LoginForm()
            return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = CustomUser.objects.get(email=email)

            except CustomUser.DoesNotExist:
                messages.error(request, "User does not exist.")
                return render(request, self.template_name, {"form": form})

            if user.check_password(password):
                request.session["user_id"] = str(user.id)
                request.user = user
                return redirect(home_url)
            else:
                messages.error(request, "Email or password is incorrect.")
                return render(request, self.template_name, {"form": form})


class UserLogout(TemplateView):
    def get(self, request):
        if "user_id" in request.session:
            del request.session["user_id"]

        return redirect(home_url)


class DeleteAccount(TemplateView):
    def get(self, request, id):
        if request.user and request.user.is_authenticated:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return redirect(login_url)


class CreateBlog(TemplateView):
    def get(self, request):

        if request.user and request.user.is_authenticated:
            form = BlogForm()
            return render(request, self.template_name, {"form": form})
        else:
            return redirect(login_url)

    def post(self, request):
        form = BlogForm(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()

            return redirect(home_url)
        return render(request, self.template_name, {"form": form})


class EditBlog(TemplateView):

    template_name = None

    def get(self, request, id):
        user = Blog.objects.get(id=id)

        form = BlogForm(instance=user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog.save()
            return redirect(userprofile_url)


class DeatilBlog(TemplateView):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        form = CommentForm()
        comments = blog.comments.filter(parent__isnull=True).order_by("-created_at")
        return render(
            request,
            self.template_name,
            {"blog": blog, "form": form, "comments": comments},
        )

    def post(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog

            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()
            return redirect("blogpage", id=blog.id)

        comments = blog.comments.filter(parent__isnull=True).order_by("-created_at")
        return render(
            request,
            self.template_name,
            {"blog": blog, "form": form, "comments": comments},
        )


class DeleteBlog(TemplateView):
    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        blog.delete()
        return redirect(userprofile_url)


class Home(TemplateView):

    def get(self, request):
        if request.user and request.user.is_authenticated:
            if request.user.is_staff:
                blogs = Blog.objects.all()

                return render(
                    request,
                    "Blog/blogTemplate/admin_dashboard.html",
                    {
                        "blogs": blogs,
                    },
                )

        category_id = request.GET.get("category")
        blogs = Blog.objects.filter(status="approved")

        if category_id:
            blogs = blogs.filter(category__id=category_id)

        categories = Category.objects.all()
        return render(
            request,
            self.template_name,
            {
                "user": request.user,
                "blogs": blogs,
                "categories": categories,
                "selected_category": category_id if category_id else None,
            },
        )


class UserProfile(TemplateView):

    def get(self, request):
        if request.user and request.user.is_authenticated:
            id = request.user
            blogs = Blog.objects.filter(user=id)

            return render(
                request,
                self.template_name,
                {
                    "blogs": blogs,
                },
            )
        else:
            return redirect(login_url)


class AddCategory(TemplateView):

    def get(self, request):

        if request.user and request.user.is_authenticated:
            if request.user.is_staff:
                form = CategoryForm()
                category = Category.objects.all()
                return render(
                    request,
                    self.template_name,
                    {"form": form, "categories": category},
                )
            else:
                return redirect(login_url)

    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

        return render(
            request,
            self.template_name,
            {"form": form, "categories": Category.objects.all()},
        )


class ListCategory(TemplateView):

    def get(self, request):

        if request.user and request.user.is_authenticated:
            if request.user.is_staff:
                category = Category.objects.all()
                return render(request, self.template_name, {"category": category})
            else:
                return redirect(login_url)


class DeleteCategory(TemplateView):

    def get(self, request, id):

        category = Category.objects.get(id=id)
        category.delete()
        return redirect(category_url)


class Aprove_blog(TemplateView):

    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        blog.status = "approved"
        blog.save()
        return redirect(home_url)


class Reject_blog(TemplateView):

    def get(self, request, id):
        blog = get_object_or_404(Blog, id=id)
        blog.status = "reject"
        blog.save()
        return redirect(home_url)


class LikeBlog(TemplateView):

    def get(self, request, id):
        if request.user and request.user.is_authenticated:
            blog = get_object_or_404(Blog, id=id)
            like, created = Like.objects.get_or_create(user=request.user, blog=blog)
            if not created:
                like.delete()
            return redirect(home_url, blog_id=blog.id)
        else:
            return redirect(login_url)


class CommentBlog(TemplateView):
    template_name = "Blog/blogTemplate/comment.html"

    def get(self, request, id):
        form = CommentForm()

        return render(request, self.template_name, {"form": form})

    def post(self, request, id):

        blog = get_object_or_404(Blog, id=id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect(blog_page, id=id)
        return render(request, self.template_name, {"form": form, "blog": blog})

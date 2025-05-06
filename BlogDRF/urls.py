from django.urls import path

from Blog import views
from BlogDRF.views import auth_views, blog_views, category_views

urlpatterns = [
    path("blogs/", blog_views.BlogList.as_view(), name="blog-list"),
    path("blogs/<uuid:pk>/", blog_views.BlogDetail.as_view(), name="blog-detail"),
    path(
        "blogs/approve/<uuid:pk>/",
        blog_views.BlogApproved.as_view(),
        name="blog-approve",
    ),
    path(
        "blogs/reject/<uuid:pk>/", blog_views.BlogRejected.as_view(), name="blog-reject"
    ),
    path("likes/<uuid:pk>/", blog_views.BlogLike.as_view(), name="blog-like"),
    path("comment/<uuid:pk>/", blog_views.BlogComment.as_view(), name="blog-like"),
    path("signup/", auth_views.RegisterView.as_view(), name="signup_user"),
    path("login/", auth_views.LoginView.as_view(), name="login_user"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout_user"),
    path(
        "password-reset/request/",
        auth_views.PasswordResetRequestView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("categories/", category_views.CategoryView.as_view(), name="category-view"),
    path(
        "categories/<uuid:pk>/",
        category_views.CategoryDelete.as_view(),
        name="category-delete",
    ),
]

from django.urls import path

from Blog import views

urlpatterns = [
    path(
        "signup/",
        views.UserSigup.as_view(template_name="Blog/UserAuth/signup.html"),
        name="signup",
    ),
    path(
        "login/",
        views.UserLogin.as_view(template_name="Blog/UserAuth/login.html"),
        name="login",
    ),
    path("logout/", views.UserLogout.as_view(), name="logout"),
    path(
        "deleteAccout/<uuid:id>/",
        views.DeleteAccount.as_view(),
        name="deleteAccount",
    ),
    path(
        "forgot-password/",
        views.Custom_password_reset_request.as_view(
            template_name="Blog/UserAuth/password_reset_request.html"
        ),
        name="custom_password_reset",
    ),
    path(
        "reset-password/<uidb64>/<token>/",
        views.custom_password_reset_confirm,
        name="custom_password_reset_confirm",
    ),
    path(
        "add/",
        views.CreateBlog.as_view(template_name="Blog/blogTemplate/add_blog.html"),
        name="addblog",
    ),
    path(
        "update/<uuid:id>/",
        views.EditBlog.as_view(template_name="Blog/blogTemplate/updateblog.html"),
        name="updateblog",
    ),
    path("delete/<uuid:id>/", views.DeleteBlog.as_view(), name="deleteblog"),
    path(
        "blogDetail/<uuid:id>/",
        views.DeatilBlog.as_view(template_name="Blog/blogTemplate/blog_page.html"),
        name="blogpage",
    ),
    path(
        "userblog/",
        views.UserProfile.as_view(template_name="Blog/blogTemplate/blog_list.html"),
        name="blogList",
    ),
    path(
        "home/",
        views.Home.as_view(template_name="Blog/blogTemplate/Home.html"),
        name="profile",
    ),
    path(
        "approveblog/<uuid:id>/",
        views.Aprove_blog.as_view(),
        name="approve_blog",
    ),
    path(
        "rejectedblog/<uuid:id>/",
        views.Reject_blog.as_view(),
        name="reject_blog",
    ),
    path(
        "Category/",
        views.AddCategory.as_view(template_name="Blog/blogTemplate/category.html"),
        name="addCategory",
    ),
    path(
        "deleteCategory/<uuid:id>",
        views.DeleteCategory.as_view(template_name="Blog/blogTemplate/category.html"),
        name="deleteCategory",
    ),
    path(
        "like/<uuid:id>/",
        views.LikeBlog.as_view(template_name="Blog/blogTemplate/Home.html"),
        name="like_blog",
    ),
    # path(
    #     "add_comment/<uuid:id>/",
    #     views.CommentBlog.as_view(
    #         template_name="Blog/blogTemplate/comment.html"
    #     ),
    #     name="add_comment",
    # ),
]

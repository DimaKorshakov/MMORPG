from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('post/<slug:post_slug>/new_comment/', NewComment.as_view(), name='new_comment'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ShowCategory.as_view(), name='category'),
    path('register/', signup, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('new_post/', CreatePost.as_view(), name='create'),
    path('user_post/', Home.post_user, name='user_post'),
    path('comment/', Comments.as_view(), name='user_comment'),
    path('comment/<slug:comment_slug>/', ShowComment.as_view(), name='comment'),

]

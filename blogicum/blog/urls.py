from django.urls import path
from .views import PostListView, PostDetail, CategoryPostList, \
    PostCreateView, PostDeleteView, PostUpdateView, CommentDeleteView
from users.views import UserDetailView, UserUpdateView
from .views import CommentCreateView, CommentUpdateView

app_name = 'blog'

urlpatterns = [
    path('',
         PostListView.as_view(),
         name='index'),
    path('profile/<str:username>/',
         UserDetailView.as_view(),
         name='profile'),
    path('profile/edit',
         UserUpdateView.as_view(),
         name='edit_profile'),
    path('category/<slug:category_slug>/',
         CategoryPostList.as_view(),
         name='category_posts'),
    path('posts/create/',
         PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/',
         PostUpdateView.as_view(),
         name='edit_post'),

    path('posts/<int:post_id>/',
         PostDetail.as_view(),
         name='post_detail'),
    path('posts/<int:post_id>/delete/',
         PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/',
         CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         CommentDeleteView.as_view(),
         name="delete_comment", )
]

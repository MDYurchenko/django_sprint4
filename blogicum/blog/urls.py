from django.urls import path
from .views import post_detail, PostListView, PostDetail, CategoryPostList, \
    PostCreateView, PostUpdateView
from users.views import UserDetailView
from .views import CommentCreateView, CommentUpdateView

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    # path('posts/<int:post_id>/',          post_detail,         name='post_detail'),
    # path('category/<slug:category_slug>/', category_posts, name='category_posts')
    path('category/<slug:category_slug>/', CategoryPostList.as_view(), name='category_posts'),
    path('posts/create/', PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('profile/<username>/', UserDetailView.as_view(), name='profile'),
    path('posts/<int:post_id>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comment/', CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<post_id>/edit_comment/<comment_id>/', CommentUpdateView.as_view(),
         name='edit_comment'
         )
]

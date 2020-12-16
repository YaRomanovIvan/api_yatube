from posts.views import PostViewSet, CommentViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views


router = DefaultRouter()
router.register("posts", PostViewSet, basename="Post")
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="Comment"
)

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls)),
]

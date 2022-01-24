from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="homepage"),
    path("subscription/",
         RegisteredHomePageView.as_view(), name="subhomepage"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("genre_selection/", add_subscription_categories, name="genre_selection"),
    path("edit_genre_selection/", edit_subscription_categories, name="edit_genre_selection"),
    path('search_episodes/', search_episodes, name='search_episodes'),
    path('like/', like, name='episode-like'),
    path('user_favorites/', UserFavoriteListView.as_view(), name='user_favorites'),
]

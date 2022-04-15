from django.contrib import admin
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView

import gametime_auth.views
#import games.views
from gametime_auth.forms import RegistrationForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/profile/", gametime_auth.views.profile, name="profile"),
    path(
        "accounts/register/",
        RegistrationView.as_view(form_class=RegistrationForm),
        name="django_registration_register",
    ),
    path("accounts/", include("django_registration.backends.activation.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    #path("", game.views.index),
    #path("game-times/", game.views.game_time_list, name="game_time_list_ui"),
    #path("game-times/<int:pk>/",games.views.game_time_detail,name="game_time_detail_ui",),
    #path("search/", games.views.game_search, name="game_search_ui"),
    #path("games/<slug:imdb_id>/", games.views.game_detail, name="game_detail_ui"),
    path("api/v1/", include("config.api_urls")),
]

from django.contrib import admin

from games.models import Game, GameTime, GameTimeInvitation, SearchTerm, Genre

admin.site.register(Game)
admin.site.register(GameTime)
admin.site.register(GameTimeInvitation)
admin.site.register(SearchTerm)
admin.site.register(Genre)

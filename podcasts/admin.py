from django.contrib import admin

# Register your models here.
from .models import Episode, Category, User, Favorite
from django.contrib.auth.admin import UserAdmin

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", "title", "published_date")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)



@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # fields = ["genres"]
    list_display = ("username", "email", "get_genres",)
    def get_genres(self, obj):
        return ", ".join([p.title for p in obj.genres.all()])

    # def get_favorites(self):
    #     if self.user:
    #         return self.user.favorite_set.all()
    get_genres.short_description = "GENRES"
    # list_display = ("username", "email", "followed_genre",
    #                 "genres_list", "following_genres")
    # genres = Category.objects.all()
    # print(genres)
    # list_filter = ("genres")
    # fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('genres','favorites')}),)
    # add_fieldsets = UserAdmin.add_fieldsets + \
    #     ((None, {'fields': ('genres','favorites')}),)
    fieldsets = UserAdmin.fieldsets + \
        ((None, {'fields': ('genres', )}),)
    add_fieldsets = UserAdmin.add_fieldsets + \
        ((None, {'fields': ('genres', )}),)

admin.site.register(Favorite)

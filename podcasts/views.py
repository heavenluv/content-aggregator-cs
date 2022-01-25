from http.client import HTTPResponse
from django.views.generic import ListView
from .models import Episode, Favorite, User
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from podcasts.forms import CustomUserCreationForm
# Create your views here.
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from podcasts.forms import GenreSelectionForm
from django.http import HttpResponseRedirect, HttpResponse
import json

@login_required
def add_subscription_categories(request):
    current_user = request.user
    if current_user.genres.exists():
        return redirect(reverse("subhomepage"))
    # print(current_user)
    if request.method == "POST":
        form  = GenreSelectionForm(request.POST)
        if form.is_valid():
            current_user.genres.set(form.cleaned_data["available_options"])
            current_user.save()
            return HttpResponseRedirect(reverse_lazy("subhomepage"))
            # return HttpResponse('<h1>Page was found</h1>')
    else:
        form = GenreSelectionForm()
        
    context = {
        "form": form,
        "user_instance": current_user,
    }
    return render(request, "genre_selection.html", context)


@login_required
def edit_subscription_categories(request):
    current_user = request.user
    if not current_user.genres.exists():
        return HttpResponseRedirect(reverse_lazy("genre_selection"))
    if request.method == "POST":
        form = GenreSelectionForm(request.POST)
        if form.is_valid():
            current_user.genres.set(form.cleaned_data["available_options"])
            current_user.save()
            return HttpResponseRedirect(reverse_lazy("subhomepage"))
            # return HttpResponse('<h1>Page was found</h1>')
    else:
        form = GenreSelectionForm()

    context = {
        "form": form,
        "following_genres": [ obj.title for obj in current_user.genres.all()],
    }
    return render(request, "edit_genre_selection.html", context)

class HomePageView(ListView):
    paginate_by = 10
    template_name = "homepage.html"
    model = Episode
    

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        
        list_episodes = Episode.objects.filter().order_by("-published_date")
        paginator = Paginator(list_episodes, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            file_episodes = paginator.page(page)
        except PageNotAnInteger:
            file_episodes = paginator.page(1)
        except EmptyPage:
            file_episodes = paginator.page(paginator.num_pages)

        context['episodes'] = file_episodes
        return context


class RegisteredHomePageView(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = "subhomepage.html"
    model = Episode

    def search(self):
        following_genres_queryset = User.objects.filter(id=self.request.user.id)[0].genres.all()
        following_genres_list = [
            p.id for p in following_genres_queryset]
        episodes = Episode.objects.filter(
            category__in=following_genres_list).order_by("-published_date")
        return episodes


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_episodes = self.search()
        paginator = Paginator(list_episodes, self.paginate_by)
        page = self.request.GET.get('page')
        

        try:
            file_episodes = paginator.page(page)
        except PageNotAnInteger:
            file_episodes = paginator.page(1)
        except EmptyPage:
            file_episodes = paginator.page(paginator.num_pages)
        # print(paginator.num_pages)
        liked = [i for i in Episode.objects.all() if Favorite.objects.filter(
            user=self.request.user, like=i)]
        context['liked_episode'] = liked
        context['episodes'] = file_episodes
        context["page_obj"].paginator.num_pages = paginator.num_pages
        return context

# class GenreSelectionView()

# def dashboard(request):
#     return render(request, "users/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.last_login == user.date_joined or user.genres == "podcasts.Category.None":
                return HttpResponseRedirect(reverse("genre_selection"))
            return HttpResponseRedirect(reverse("subhomepage"))

@login_required
def search_episodes(request):
    query = request.GET.get('p')
    object_list = Episode.objects.filter(description__icontains=query)
    liked = [i for i in object_list if Favorite.objects.filter(
        user=request.user, like=i)]
    context = {
        'episodes': object_list,
        'liked_post': liked
    }
    return render(request, "search_episodes.html", context)


@login_required
def like(request):
    # print("\n\n\n\n\n")
    # print("POST: ")
    # print(request.POST)
    # print("GET: ")
    # print(request.GET)
    
    # print("\n\n\n\n\n")
    episode_id = request.GET.get("likeId", "")
    user = request.user
    episode = Episode.objects.get(id=episode_id)
    liked = False
    like = Favorite.objects.filter(user=user, like=episode)
    if like:
        like.delete()
    else:
        liked = True
        Favorite.objects.create(user=user, like=episode)
    resp = {
            'liked': liked
        }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


class UserFavoriteListView(LoginRequiredMixin, ListView):
    model = Episode
    template_name = 'user_favorites.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserFavoriteListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.request.user.id)
        liked = [i for i in Episode.objects.all() if Favorite.objects.filter(user=self.request.user, like=i)]
        paginator = Paginator(liked, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            liked_episodes = paginator.page(page)
        except PageNotAnInteger:
            liked_episodes = paginator.page(1)
        except EmptyPage:
            liked_episodes = paginator.page(paginator.num_pages)
        context['liked_episode'] = liked_episodes
        context["page_obj"].paginator.num_pages = paginator.num_pages
        return context

    # def get_queryset(self):
    #     user = get_object_or_404(User, id=self.request.user.id)
    #     return Episode.objects.filter().order_by("-published_date")

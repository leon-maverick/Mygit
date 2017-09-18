from django.views import generic
from django.views.generic import FormView, RedirectView
from .models import Album, Song, Game
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm
from rest_framework.views import APIView
from .serializers import GameSerializer
from rest_framework.response import Response
from .models import Game
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
            'name': str(request.user.first_name),
            'email': str(request.user.email),
            'pass': str(request.user.password),

        }
        return Response(content)

class GameList(APIView):
    def get (self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response (serializer.data)
        #return serializer.data

    def post (self):
        pass

class IndexView(generic.ListView):
    template_name = 'music/index.html'

    def get_queryset(self):
        return Album.objects.all()

class BoxcarsView(generic.ListView):
    template_name = 'music/Boxcars.html'
    def get_queryset(self):
         return Game.objects.all()

class DetailView (generic.DetailView):
    model = Album
    template_name = 'music/detail.html'

class AlbumCreate (CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumUpdate (UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']

class AlbumDelete (DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # dispaly new form for register
    def get(self, request):
        form = self.form_class(None)
        return  render(request, self.template_name, {'form':form})

    # process form data
    def post (self, request):
        print("1")
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False) # just store it normally
            # clean and normalize data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #email = form.cleaned_data['email']
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            user.set_password(password)
            user.save()
            print("2")

            # return user objects if credentials are correct
            user = authenticate(username = username, password = password)
            if user is not None :
                print("3")
                #if user.is_active :
                login(request, user)
                return redirect('music:index')
        return render(request, self.template_name, {'form': form})

class UserFormLogin(View):
    form_class = UserForm
    template_name = 'music/login_form.html'

    # dispaly new form for login
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        print("1")
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = authenticate(request, username=username, password=password, email=email)
        form = self.form_class(request.POST)
        if user is not None:
            print("3")
            # if user.is_active :
            login(request, user)
            return redirect('music:index')
        return render(request, self.template_name, {'form': form})

class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/music/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

def logout_view(request):
    logout(request)


class GamesView(generic.ListView):
    template_name = 'music/games.html'
    def get_queryset(self):
        return Game.objects.all()


'''
from django.shortcuts import render, get_object_or_404
from .models import Album, Song

def index (request):
    all_albums = Album.objects.all()
    return  render(request,'music/index.html', {'all_albums': all_albums})

def detail (request, album_id):
    album = get_object_or_404(Album, pk= album_id)
    songs = Song.objects.filter(album=album_id)
    return render(request,'music/detail.html', {'album': album, 'songs':songs})

def favorite (request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.song_set.get (pk=request.POST['song'])
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
            'album':album,
            'error_massage': "You did not select the valid song",
        })
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return  render(request, 'music/detail.html', {'album': album})
'''
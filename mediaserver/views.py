from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import mediaDatabase
from .models import fs
from django.views.static import serve

import os
import omdb
import datetime
import requests
import urllib.request
from PIL import Image
from youtube_api import YoutubeDataApi
#import settings
from Binge.settings import MEDIA_ROOT
from Binge.settings import MOVIE_STORAGE_ROOT


omdb_APIKEY     = '6a913a99'
tmdb_APIKEY     = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
youtube_APIKEY  = 'AIzaSyAy3wo3cIPFZQPjNKfWjXNR7v5vdF2fF90'




# Create your views here.

def get_movie_poster(image_url, name_to_save_as):
    file_path = MEDIA_ROOT
    name_to_save_as = name_to_save_as + '_poster.jpg'
    full_path = file_path + name_to_save_as
    
    urllib.request.urlretrieve(image_url, full_path)

    img = Image.open(full_path)
    resized_img = img.resize((300,445))
    resized_img.save(full_path)

    return name_to_save_as



def get_tmdb_movie_backdrop(imdb_id, name_to_save_as):
    
    tmdb_movie_info_url  = "https://api.themoviedb.org/3/find/{}?api_key={}&language=en-US&external_source=imdb_id".format(imdb_id, tmdb_APIKEY)
    print(tmdb_movie_info_url)
    print(tmdb_movie_info_url)
    tmdb_movie_info      = requests.get(tmdb_movie_info_url)
    tmdb_movie_info      = tmdb_movie_info.json()
    

    tmdb_movie_backdrop_path = tmdb_movie_info['movie_results'][0]['backdrop_path']
    tmdb_backdrop_url        = 'http://image.tmdb.org/t/p/original{}'.format(tmdb_movie_backdrop_path)
    

    file_path       = MEDIA_ROOT
    name_to_save_as = name_to_save_as + '_backdrop.jpg'
    full_path       = file_path + name_to_save_as
    
    urllib.request.urlretrieve(tmdb_backdrop_url, full_path)

    return name_to_save_as

#def handle_uploaded_file(upload):
#    for chunk in upload.chunks():





def home(request):
    all_movies = mediaDatabase.objects.all()

    return render(request, 'index.html', {'all_movies': all_movies})



def search(request):
    movie_name = request.POST['movie']
    client = omdb.OMDBClient(apikey=omdb_APIKEY)
    #try:
    movie_data = client.title(movie_name)
    if movie_data != {}:
        if  mediaDatabase.objects.filter(title=movie_data['title']).exists():
            print('movie already exists')
        else:
            data = mediaDatabase()
            
            data.title               = movie_data['title']
            data.year                = movie_data['year']
            data.release_date        = datetime.datetime.strptime(movie_data['released'], "%d %b %Y")
            data.rated               = movie_data['rated']

            runtime                  = int(movie_data['runtime'].split(' ')[0])
            data.runtime             = datetime.timedelta(days=0, hours=runtime//60, minutes=runtime%60)

            data.genre               = movie_data['genre']
            data.director            = movie_data['director']
            data.writers             = movie_data['writer']
            data.cast                = movie_data['actors']
            data.plot                = movie_data['plot']

            movie_poster_url         = movie_data['poster']
            print(movie_poster_url)
            #movie_backdrop_url       = movie_data['backdrop']
            #print(movie_data['imdb_id'])

            data.poster              = get_movie_poster(movie_poster_url, movie_data['title'])
            data.backdrop            = get_tmdb_movie_backdrop(movie_data['imdb_id'], movie_data['title'])
                    
            metascore                = int(movie_data['metascore'])
            data.ratings_metacritic  = metascore

            imdb_value               = float(movie_data['imdb_rating'])
            data.ratings_imdb        = imdb_value

            rt_value                 = movie_data['ratings'][1]
            rt_value                 = int(rt_value['value'].split('%')[0])
            data.ratings_rotten      = rt_value

            data.ratings_average     = int((metascore + rt_value + (imdb_value*10))/3)

            if request.FILES:
                uploaded_file = request.FILES['movie_file']
                
                uploaded_file_name = fs.save(uploaded_file.name, uploaded_file)
                print(uploaded_file_name)
                data.movie_path = os.path.join(MOVIE_STORAGE_ROOT, uploaded_file_name) 

            data.save()
            
            
        
        #except:
        #    print('Check your internet connection')
    

    return redirect('/')



def addmovie(request):
    
    return render(request, 'addmovie.html')
    #return redirect('/addmovie/')



def moviedetails(request):
    try:
        movie_title = request.GET['movie_title']
        movie = mediaDatabase.objects.get(title=movie_title)
        return render(request, 'moviedetails.html', {'moviedetails':movie})
    except:
        return redirect('/')


def watchtrailer(request):
    movie_title = request.GET['movie_title']
    movie_year = request.GET['movie_year']
    #print(movie_year)
    #print(movie_title)
    yt = YoutubeDataApi(youtube_APIKEY)
    movie_trailer_search = yt.search(movie_title + ' ' + str(movie_year) + ' trailer', max_results=1)
    movie_trailer_search = movie_trailer_search[0]
    movie_trailer_id = movie_trailer_search['video_id']
    return redirect('https://www.youtube.com/watch?v=' + movie_trailer_id)


def playmovie(request):
    movie_title = request.GET['movie_title']
    movie = mediaDatabase.objects.get(title=movie_title)
    movie_path = movie.movie_path
    #os.startfile(movie_path)
    #return redirect('/')
    return serve(request, os.path.basename(movie_path), os.path.dirname(movie_path))
    
    


video_file_ext = ('.webm','.mpg','.mp2','.mpeg','.mpe','.mpv','.ogg','.mp4','.m4p','.m4v','.avi','.wmv','.mov','.qt','.flv','.swf')
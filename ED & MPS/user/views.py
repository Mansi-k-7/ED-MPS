from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .utility.GetImageStressDetection import ImageExpressionDetect
from .models import *

import os
import random
import pygame

# Create your views here.
def Userregister(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('contact')
        form = userregistermodel(name=name, email=email, password=password, phoneno=phone,  status='waiting')
        form.save()
        messages.success(request, 'Registration Successful')
        return render(request, 'index.html')
    else:
        messages.error(request, 'Registration Un-Successful')
        return render(request, 'index.html')      
    
def userhome(request):
    email = request.session['email']
    data = userimagepredictionmodel.objects.filter(email=email)
    return render(request, 'user/userhome.html', {'data':data})

def userlogout(request):
    return render(request, 'index.html')

def UploadImageAction(request):
    image_file = request.FILES['file']
    if not image_file.name.endswith('.jpg'):
        messages.error(request, 'THIS IS NOT A JPG  FILE')

    fs = FileSystemStorage()
    filename = fs.save(image_file.name, image_file)
    uploaded_file_url = fs.url(filename)
    obj = ImageExpressionDetect()
    emotion = obj.getExpression(filename)
    print(emotion)
    music_status = play_music(emotion)
    email = request.session['email']
    userimagepredictionmodel.objects.create(email=email, emotion=emotion, filename=filename, file=uploaded_file_url) 
    data = userimagepredictionmodel.objects.filter(email=email)
    return render(request, 'user/userhome.html', {'data':data, 'music_playing': music_status})

def UserLiveCameDetect(request):
    obj = ImageExpressionDetect()
    obj.getLiveDetect()
    email = request.session['email']
    data = userimagepredictionmodel.objects.filter(email=email)
    return render(request, 'user/userhome.html', {'data':data})

def play_music(emotion):
    # Map emotions to music directories
    emotion_paths = {
        'Angry': 'assets/music/Angry',
        'Disgusted': 'assets/music/Disgusted',
        'Fear': 'assets/music/Fear',
        'Happy': 'assets/music/Happy',
        'Neutral': 'assets/music/Neutral',
        'Surprised': 'assets/music/Surprised',
    }

    # Check if the given emotion is valid
    if emotion not in emotion_paths:
        print(f"Invalid emotion: {emotion}. Please choose a valid emotion.")
        return False

    # Construct the music path
    music_path = emotion_paths[emotion]

    try:
        # List all .mp3 files in the directory
        music_files = [f for f in os.listdir(music_path) if f.endswith('.mp3')]
        
        # Check if there are any music files
        if not music_files:
            print(f"No music files found in {music_path}.")
            return False

        # Choose a random music file
        random_music_file = random.choice(music_files)
        music_full_path = os.path.join(music_path, random_music_file)

        # Initialize mixer and play the music
        pygame.mixer.init()
        pygame.mixer.music.load(music_full_path)
        pygame.mixer.music.play()

        return True

    except FileNotFoundError:
        print(f"The directory {music_path} does not exist.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def stop_music(request):
    if request.method == 'POST':
        pygame.mixer.music.stop()
        email = request.session['email']
        data = userimagepredictionmodel.objects.filter(email=email)
        return render(request, 'user/userhome.html', {'data':data})
    else:
        email = request.session['email']
        data = userimagepredictionmodel.objects.filter(email=email)
        return render(request, 'user/userhome.html', {'data':data})
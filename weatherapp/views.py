from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    cities = City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c834efb84c6315bba71d237277828930'

    err_msg=''
    message=''
    message_class=''
    
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            
            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save() 
                else:
                    err_msg='City  does not exists in the world!'
            else:
                err_msg='City already exists in the database!'

        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City added successfully'
            message_class='is-success'        

            # will validate and save if validate

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list
    
    context = {'weather_data' : weather_data, 'form' : form,'message':message,'message_class':message_class}
    cities = City.objects.all().delete()

    return render(request, 'weather/index.html', context) #returns the index.html template

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
from django.shortcuts import render
import requests

def index(request):
    """
    Main view: Serves the global wind field (from local file)
    AND handles clicked real-time pin-point data.
    """
    
    # 1. Replace with your actual OWM API key
    # (Do this for both views, as per previous instructions)
    api_key = 'a789653a54979b820b7bb9637d404731'
    
    # 2. DEFAULT CITY: The search bar logic stays for now
    city = request.GET.get('city', 'London')
    
    # URL to fetch current weather details for the searched city
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url).json()
    
    weather_data = {}
    if response.get('cod') == 200:
        weather_data = {
            'city': response['name'],
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'lat': response['coord']['lat'],
            'lon': response['coord']['lon'],
        }
    else:
        weather_data = {'error': 'City not found!'}

    # 3. Handle a real-time coordinate request for clicked pins
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    real_time_spot_data = {}
    if lat and lon:
        url_coord = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        resp_coord = requests.get(url_coord).json()
        if resp_coord.get('cod') == 200:
            real_time_spot_data = {
                'city': resp_coord['name'],
                'temperature': resp_coord['main']['temp'],
                'description': resp_coord['weather'][0]['description'],
                'icon': resp_coord['weather'][0]['icon'],
                'speed': resp_coord['wind']['speed'],  # Get the raw speed
                'deg': resp_coord['wind']['deg']      # Get the wind degree/angle
            }
        
    return render(request, 'weather/index.html', {
        'weather_data': weather_data,
        'real_time_spot_data': real_time_spot_data
    })
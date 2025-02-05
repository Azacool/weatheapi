from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import WeatherData
from .serializers import UserSerializer, WeatherDataSerializer
import requests



@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather(request, city):
    API_KEY = 'your_weather_api_key'
    url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return Response({'error': 'City not found'}, status=404)
    
    data = response.json()
    weather_data = {
        'name': data['location']['name'],
        'country': data['location']['country'],
        'lat': data['location']['lat'],
        'lon': data['location']['lon'],
        'temp_c': data['current']['temp_c'],
        'wind_kph': data['current']['wind_kph'],
        'cloud': data['current']['cloud'],
        'temp_color': get_temp_color(data['current']['temp_c']),
        'wind_color': get_wind_color(data['current']['wind_kph']),
        'cloud_color': get_cloud_color(data['current']['cloud'])
    }
    
    WeatherData.objects.create(**weather_data)
    return Response(weather_data)

def get_temp_color(temp):
    if temp <= -30:
        return '#003366'
    elif temp <= -20:
        return '#4A90E2'
    elif temp <= -10:
        return '#B3DFFD'
    elif temp <= 0:
        return '#E6F7FF'
    elif temp <= 10:
        return '#D1F2D3'
    elif temp <= 20:
        return '#FFFACD'
    elif temp <= 30:
        return '#FFCC80'
    elif temp <= 40:
        return '#FF7043'
    else:
        return '#D32F2F'
    

def get_wind_color(wind_kph):
    if wind_kph <= 10:
        return '#E0F7FA'
    elif wind_kph <= 20:
        return '#B2EBF2'
    elif wind_kph <= 40:
        return '#4DD0E1'
    elif wind_kph <= 60:
        return '#0288D1'
    else:
        return '#01579B'

def get_cloud_color(cloud):
    if cloud <= 10:
        return '#FFF9C4'
    elif cloud <= 30:
        return '#FFF176'
    elif cloud <= 60:
        return '#E0E0E0'
    elif cloud <= 90:
        return '#9E9E9E'
    else:
        return '#616161'

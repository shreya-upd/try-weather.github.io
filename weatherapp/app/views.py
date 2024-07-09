# from django.shortcuts import render
# import requests
# import datetime

# def home(request):
#     if request.method == 'POST':
#         city = request.POST.get('city', 'Kathmandu')
#     else:
#         city = 'Kathmandu'
    
#     url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=dc6d6c7828060d4e165260706377d388'
#     PARAMS = {'units': 'metric'}
  
#     response = requests.get(url, params=PARAMS)
    
#     if response.status_code == 200:
#         data = response.json()
#         if 'weather' in data:
#             description = data['weather'][0].get('description', 'Weather description not available')
#             icon = data['weather'][0].get('icon', '')
#             temp = data['main'].get('temp', 'Temperature not available')
#             day = datetime.date.today()
#             return render(request, 'app/index.html', {'city': city,'description': description, 'icon': icon, 'temp': temp, 'day': day})
#         else:
#             return render(request, 'app/index.html', {'city': city,'description': 'Weather data not available', 'icon': '', 'temp': '', 'day': datetime.date.today()})
#     else:
#         return render(request, 'app/index.html', {'city': city,'description': f"Failed to fetch data. Status code: {response.status_code}", 'icon': '', 'temp': '', 'day': datetime.date.today()})









from django.shortcuts import render
import requests
import datetime

def home(request):
    default_city = 'Kathmandu'

    if request.method == 'POST':
        city = request.POST.get('city', default_city)
    else:
        city = default_city
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=dc6d6c7828060d4e165260706377d388'
    PARAMS = {'units': 'metric'}
  
    try:
        response = requests.get(url, params=PARAMS)
        response.raise_for_status()  # Raise an HTTPError for bad responses (e.g., 404, 500)
        data = response.json()
        if 'weather' in data:
            description = data['weather'][0].get('description', 'Weather description not available')
            icon = data['weather'][0].get('icon', '')
            temp = data['main'].get('temp', 'Temperature not available')
            day = datetime.date.today()
            return render(request, 'app/index.html', {'city': city, 'description': description, 'icon': icon, 'temp': temp, 'day': day})
        else:
            error_message = f"City '{city}' is not available from the Weather API. Showing weather for '{default_city}'."
            city = default_city
    except requests.exceptions.HTTPError as e:
        error_message = f"Failed to fetch data for city '{city}' from the Weather API. Showing weather for '{default_city}'. Error: {e}"
        city = default_city
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        city = default_city
    
    return render(request, 'app/index.html', {'city': city, 'error_message': error_message})

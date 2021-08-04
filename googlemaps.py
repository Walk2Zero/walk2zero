import requests
import pprint as pp

origins = input("Your location: ")
destination = input("Your destination: ")
mode = input("You preferred travel mode: ")


def get_distance(origins, destinations, mode):
    api_key = "Your API Key"
    uri = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&mode={mode}&key={api_key}&language=en-GB'
    response = requests.get(uri)

    output = response.json()

    pp.pprint(output)

    for obj in output['rows']:
        for data in obj['elements']:
            print(data['distance']['text'])

get_distance(origins, destination, mode)

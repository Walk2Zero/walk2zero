import requests


def input_locations():
    """
    This allows the user to input the locations of the origin and destination, assigns them to variables and returns
    these variables.

    :return: inputted origins and destination
    """
    origin = input("Your location: ")
    destination = input("Your destination: ")
    return origin, destination


def get_distance(origin, destination):
    """
    This function takes the inputted origin and destination, then uses the google maps API to calculate the distances
    and duration (take out if not needed) of the route. These are outputted for each mode of transport so they are all
    available.

    :param origin: inputted origin
    :type origin: string
    :param destination: inputted destination
    :type destination: string
    :return: origin address, destination address and distances & durations of route for each mode of transport.
    """
    api_key = "Your API key here"
    modes = ["driving", "walking", "bicycling", "transit"]
    distances = dict()
    durations = dict()
    for mode in modes:
        uri = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
              f'origins={origin}&' \
              f'destinations={destination}&' \
              f'mode={mode}&' \
              f'key={api_key}&language=en-GB'

        response = requests.get(uri)
        output = response.json()

        origin_address = output['origin_addresses']
        destination_address = output['destination_addresses']

        for obj in output['rows']:
            for data in obj['elements']:
                distance = data['distance']['text']
                duration = data['duration']['text']

        distances[mode] = distance
        durations[mode] = duration

    return origin_address, destination_address, distances, durations


origin, destination = input_locations()
origin_address, destination_address, distances, durations = get_distance(origin, destination)
print(f'origin address: {origin_address}')
print(f'destination address: {destination_address}')
print(distances)
print(durations)

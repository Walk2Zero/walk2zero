short_distances = {'driving': '4.7 km', 'walking': '4.0 km', 'bicycling': '5.6 km', 'transit': '5.2 km'}
long_distances = {'driving': '4.7 km', 'walking': '7.0 km', 'bicycling': '5.6 km', 'transit': '5.2 km'}
super_distances = {'driving': '2,205 km', 'walking': '2,188 km', 'bicycling': '2,296 km', 'transit': '2,543 km'}


def str_to_float(distances):
    """
    Function to change the string distances in in the dictionary distances from the API and changes them into floats
    without "km".

    :param distances: distances as dictionary (as would be received from the function get_distance())
    :return: distances as dictionary where the values are floats of the distance (km)
    """
    for key, value in distances.items():
        value = value.replace(',', '')
        distances[key] = float(value[:-3])
    return distances


def propose_modes(distances):
    """
    This function removes the "walking" mode, from the distances dictionary,if the distance of the journey is greater
    than 5km as will no longer be a viable mode of transport.

    :param distances: distances as dictionary (as would be received from the function get_distance())
    :return: distances as dictionary only including the viable modes of transport
    """
    distances = str_to_float(distances)
    if distances['walking'] > 5:
        del distances['walking']

    return distances


print(propose_modes(short_distances))
print(propose_modes(long_distances))
print(propose_modes(super_distances))
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
    if distances['bicycling'] > 100:
        del distances['bicycling']

    return distances


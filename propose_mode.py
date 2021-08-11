short_distances = {'driving': '4.7 km', 'walking': '4.0 km', 'bicycling': '5.6 km', 'transit': '5.2 km'}
long_distances = {'driving': '4.7 km', 'walking': '7.0 km', 'bicycling': '5.6 km', 'transit': '5.2 km'}
super_distances = {'driving': '2,205 km', 'walking': '2,188 km', 'bicycling': '2,296 km', 'transit': '2,543 km'}


def str_to_float(distances):
    for key, value in distances.items():
        value = value.replace(',', '')
        distances[key] = float(value[:-3])
    return distances


def propose_modes(distances):
    distances = str_to_float(distances)
    if distances['walking'] > 5:
        del distances['walking']

    return distances


print(propose_modes(short_distances))
print(propose_modes(long_distances))
print(propose_modes(super_distances))
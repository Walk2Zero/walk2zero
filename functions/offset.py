def offset(proposed_mode, chosen_mode):
    """
    Function takes proposed mode as one argument which is a dictionary of modes of transport based on distance,
    chosen mode as another argument which is a dictionary of one selected mode by user for that journey
    :param proposed_mode:
    :param chosen_mode:

    """
    prop_trans = max(proposed_mode, key=proposed_mode.get)
    prop_emission_max = proposed_mode.get(prop_trans)
    for key in chosen_mode:
        chosen_emission = chosen_mode.get(key)
    offset = prop_emission_max - chosen_emission

    return offset


print(offset({'a': 5, 'b': 5, 'c': 15.156, 'd': 100},
       {'d': 100}))


print(offset({'a': 5, 'b': 5, 'c': 15.156, 'd': 100},
       {'a': 5}))




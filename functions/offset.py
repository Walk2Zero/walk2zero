def offset(proposed_mode,chosen_mode):
   """
   Function takes proposed mode as one argument which is a dictionary of modes of transport based on distance,
   chosen mode as another argument which is a dictionary of one selected mode by user for that journey
   :param proposed_mode:
   :param chosen_mode:

   """
   prop_trans=max(proposed_mode, key=proposed_mode.get)
   prop_emission_max= proposed_mode.get(prop_trans)
   #print(prop_emission_max)
   for key in chosen_mode:
     chose_emission= chosen_mode.get(key)
   #print(chose_emission)
   def emission_return(prop_emission_max,chose_emission):
       """
       This function calculates offset(difference of carbon consumed/saved) and returns
       offset of carbon consumed/saved for that journey
       :param proposed emission max
       :param chosen mode emission
       :return offset
        """
       offset=prop_emission_max-chose_emission
       if offset==0:
           print("You have contributed ZERO carbon emission, NO EMISSION NO SAVING")
       elif offset>0:
           offset = format(offset, ".3f")
           print("You have consumed "+str(offset)+" grams of carbon, BETTER LUCK NEXT TIME")
       elif offset<0:
           offset = format(offset, ".3f")
           offset=str(offset).lstrip('-')
           print("Wow!! You have saved "+str(offset)+" grams of carbon, Congrats ")
       return offset
   c=emission_return(prop_emission_max,chose_emission)
   print("offset="+str(c))

offset({'a':5, 'b':5, 'c':15.156, 'd':100},
        {'d':200})




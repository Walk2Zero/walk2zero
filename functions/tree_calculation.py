import colorama
from colorama import Fore
colorama.init()

def calc_trees(offset):
    """1 gram of carbon produces 3.67grams of co2
       1 tree can absorb 21,772.416 grams of co2 in its life time on an avg"""
    co2_prod= 3.67*offset
    Tree_saved=(co2_prod/(21772.416))*100
    Tree_saved=format(Tree_saved,".3f")
    print(Fore.GREEN+"YAY!! YOU HAVE SAVED "+ str(Tree_saved)+"% of a typical tree WITH THIS JOURNEY")
    return Tree_saved
calc_trees(100.00)

calc_trees(87.67)






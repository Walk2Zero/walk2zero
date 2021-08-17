import pyfiglet


class CliStyles:

    @staticmethod
    def welcome_banner():
        banner = pyfiglet.figlet_format(text="Walk 2 Zero",
                                        font="standard",
                                        justify="center")
        slogan = "C L I M A T E   C O N S C I O U S   S T E P S"
        print(f"{banner}"
              f"{slogan:^80}"
              f"\n\n(To exit enter 'q')")

    @staticmethod
    def user_main_menu():

        print("Please select from the following options:\n\n"
              "    (1) plan journey\n"
              "    (2) view user stats\n"
              "    (3) register a vehicle\n"
              "    (4) log out\n")

    @staticmethod
    def heading_1(func):
        print("\n=============================================================="
              "==================")
        func()
        print("=============================================================="
              "==================")

    @staticmethod
    def heading_2(func):
        func()
        print("\n--------------------------------------------------------------"
              "------------------")

    @staticmethod
    def line_space(func):
        func()
        print("\n")

    @staticmethod
    def thank_you():
        ty_message_l1 = "T H A N K   Y O U   F O R   T A K I N G"
        ty_message_l2 = "C L I M A T E   C O N S C I O U S   S T E P S"
        ty_message_l3 = "G O O D B Y E"
        print(f"\n{ty_message_l1:^80}"
              f"\n{ty_message_l2:^80}"
              f"\n\n{ty_message_l3:^80}")

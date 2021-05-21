class ProgressBar:
    def __init__(self, actions_to_do, prefix='Progress:', suffix='Complete', postfix='Finished'):
        self.__prefix = prefix
        self.__suffix = suffix
        self.__postfix = postfix

        self.__decimals = 1
        self.__length = 50
        self.__fill = '█'
        self.__print_end = "\r"

        self.__actions_to_do = actions_to_do
        self.__current_action = -1

    def set_actions_to_do(self, count):
        self.__actions_to_do = count

    def show_progress(self):
        self.__current_action += 1

        try:
            percent = ("{0:." + str(self.__decimals) + "f}").format(100 * (self.__current_action/float(self.__actions_to_do)))
        except ZeroDivisionError:
            return

        filled_length = int(self.__length * self.__current_action // self.__actions_to_do)
        bar = self.__fill * filled_length + '-' * (self.__length - filled_length)

        print(f'\r{self.__prefix} |{bar}| {percent}% {self.__suffix}', end=self.__print_end)

        if self.__actions_to_do == self.__current_action:
            print()

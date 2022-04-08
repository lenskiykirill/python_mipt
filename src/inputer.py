class inputer:
    def __init__(self):
        pass

    def get_action(self):
        act = input()

        if act.isnumeric():
            return ("option", int(act)-1)

        return ("spell", act)

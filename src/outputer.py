import os

class outputer:
    def __init__(self):
        self.text    = ""
        self.chars   = list()
        self.objects = list()
        self.options = list()

    def add_char(self, name, value):
        self.chars.append((name, value))

    def add_object(self, obj):
        self.objects.append(obj)

    def add_text(self, text):
        self.text += text

    def add_option(self, opt):
        self.options.append(opt)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __get_id(self, l, s):
        left_id = (len(l) - len(s) - 2) // 2
        right_id = len(l) - len(s) - 2 - left_id

        return left_id, right_id

    def flush(self):
        self.clear()

        frame_p = "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
        frame_m = "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"

        print(frame_p)
        char_str = "Characteristics:"

        left_id, right_id = self.__get_id(frame_p, char_str)

        print('-' + ' '*left_id + char_str + ' '*right_id + '-')
        print(frame_p)

        for i in range(len(self.chars)):
            char = self.chars[i]

            char_str = char[0] + ' : ' + str(char[1])

            left_id, right_id = self.__get_id(frame_p, char_str)

            if (i % 2 == 0):
                print('-' + ' '*left_id + char_str + ' '*right_id + '-')
            else:
                print('+' + ' '*left_id + char_str + ' '*right_id + '+')

        if (len(self.chars) % 2 == 0):
            print(frame_m)
        else:
            print(frame_p)
        
        ident = len(self.chars) % 2

        obj_str = "Inventory:"

        left_id, right_id = self.__get_id(frame_p, obj_str)

        if (ident == 0):
            print('+' + ' '*left_id + obj_str + ' '*right_id + '+')
        else:
            print('-' + ' '*left_id + obj_str + ' '*right_id + '-')

        if (ident == 0):
            print(frame_m)
        else:
            print(frame_p)

        for i in range(len(self.objects)):
            obj = self.objects[i]

            left_id, right_id = self.__get_id (frame_p, obj)

            if ((i+ident) % 2 == 0):
                print('+' + ' '*left_id + obj + ' '*right_id + '+')
            else:
                print('-' + ' '*left_id + obj + ' '*right_id + '-')

        ident = (ident + len(self.objects)) % 2

        if ident == 0:
            print(frame_p)
        else:
            print(frame_m)

        print()
        
        x = 1
        for opt in self.options:
            print ('{}) '.format(x)+opt)
            x += 1

        print()

        print(self.text)

        print('> ', end='')

        self.text = ""
        self.chars = list()
        self.objects = list()
        self.options = list()

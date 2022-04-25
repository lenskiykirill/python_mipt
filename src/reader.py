import g_types

class reader:
    def __init__(self):
        pass

    def __parse_int(self, line):
        x = 0
        for c in line:
            if c == ' ':
                x += 1
            else:
                break
        
        line = line[x:]
        line = line.split(' ')[0]

        res = None

        try:
            res = int(line)
        except:
            raise ("Bad formating")

        return res

    def __parse_text(self, line):
        quote = line.find("\"")
        if quote == -1:
            raise ("Bad formating")
        line = line[quote+1:]
        slashed = False
    
        text = ""
    
        line = line.split('\n')[0]
    
        c = None
        for c in range(len(line)):
            if slashed:
                slashed = False
    
                if line[c] == '\\':
                    text += '\\'
                    continue
                
                if line[c] == 'n':
                    text += '\n'
                    continue
    
                if line[c] == 't':
                    text += '\t'
                    continue
    
                if line[c] == '\"':
                    text += '\"'
                    continue
            
            if line[c] == '\\':
                slashed = True
    
            elif line[c] == '\"':
                if (c == len(line)-1):
                    found = True
                    break
                else:
                    raise ("Bad formating")
            else:
                text += line[c]

        return text

    def get_nodes(self, source_file): # Well, here's where all fun starts!!!
        
        nodes = dict()

        node = None
        name = None

        tab_line = None

        with open(source_file) as f:
            while True:
                line = f.readline()
                if not line:
                    break

                line = line.split('#')[0]

                if line[0].isalnum():
                    if node is not None:
                        nodes[name] = node

                    node = g_types.Node ()
                    text = ""

                    if ':' not in line:
                        raise ("Bad formating")
                    
                    name = line.split(':')[0]
                    name = name.split(' ')[0]

                    continue

                if len(line) == 0:
                    continue

                if tab_line == None:
                    i = 0

                    if (line[0] == '\t'):
                        if line[1].isalpha():
                            tab_line = '\t'
                        else:
                            raise ("Bad formating")
                    elif (line[0] == ' '):
                        tab_line = ""
                        for i in range(len(line)):
                            if (line[i] == ' '):
                                tab_line += ' '
                            else:
                                if (line[i].isalpha()):
                                    break
                                else:
                                    raise ("Bad formating")

                        if i == len(line):
                            raise ("Bad formating")
                            
                if line[:len(tab_line)] == tab_line:
                    line = line[len(tab_line):]
                    line = line.split('\n')[0]
                    
                    if len(line) == 0:
                        continue

                    if ':' not in line:
                        raise ("Bad formating")

                    opt = line.split(':')[0]
                    
                    line = line[len(opt)+1:]

                    opt = opt.split(' ')[0]

                    if len(opt) == 0:
                        raise ("Bad formating")

                    if not opt[0].isalpha:
                        raise ("Bad formating")

                    opt = opt.split(' ')[0]
                    
                    if (opt == "text"):
                        text = self.__parse_text(line) 
                        node.text += text
                        continue

                    elif (opt == "option"):
                        option = g_types.Option()

                        if ':' not in line:
                            raise ("Bad formating")

                        next_n = line.split(':')[0]
                        line = line[len(next_n)+1:]
                        
                        x = 0
                        for c in next_n:
                            if c == ' ':
                                x += 1
                            else:
                                break
                        next_n = next_n[x:]
                        next_n = next_n.split(' ')[0]

                        option.node = next_n

                        option.text = self.__parse_text(line)

                        node.options.append(option)
                        continue

                    elif (opt == "action"):
                        if ':' not in line:
                            raise ("Bad formating")

                        action_type = line.split(':')[0]
                        line = line[len(action_type)+1:]

                        x = 0
                        for c in action_type:
                            if c == ' ':
                                x += 1
                            else:
                                break

                        action_type = action_type[x:]
                        action_type = action_type.split(' ')[0]

                        action = g_types.Action()

                        if action_type == "add":
                            action.action_type = action.add
                            action.object_name = self.__parse_text(line)

                        elif action_type == "remove":
                            action.action_type = action.remove
                            action.object_name = self.__parse_text(line)

                        elif action_type == "+":
                            action.action_type = action.increase_health
                            action.amount = self.__parse_int(line)

                        elif action_type == "-":
                            action.action_type = action.reduce_health
                            action.amount = self.__parse_int(line)

                        node.actions.append(action)

                    elif (opt == "spell"):
                        spell_name = None

                        if ':' not in line:
                            raise ("Bad formating")

                        next_n = line.split(':')[0]
                        line = line[len(next_n)+1:]
                        
                        x = 0
                        for c in next_n:
                            if c == ' ':
                                x += 1
                            else:
                                break
                        next_n = next_n[x:]
                        next_n = next_n.split(' ')[0]

                        spell_name = self.__parse_text(line)

                        node.spell_options[spell_name] = next_n
                        continue
        
        if node is not None:
            nodes[name] = node

        return nodes

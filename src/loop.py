import g_types
import inputer as inp
import outputer as outp
import reader as rea

source_file = "./script.src"
spell_file  = "./spells.src"
object_file = "./objects.src"

class EventLoop:
    def __init__(self):
        self.node_idx = "start"
        
        reader = rea.reader()

        self.nodes    = reader.get_nodes(source_file)
        self.inputer  = inp.inputer()
        self.outputer = outp.outputer()

#        self.spells   = reader.get_spells(spell_file)
#        self.objects  = reader.get_objects(object_file)

        self.player   = g_types.Player()

    def inner_loop(self):
        player   = self.player
        outputer = self.outputer
        inputer  = self.inputer

        node = self.nodes[self.node_idx]

        for act in node.actions:
            if (act.action_type == act.add):
                player.inventory.append(objects[act.object_name])
                continue

            if (act.action_type == act.remove):
                for it in range(len(player.inventory)):
                    obj = player.inventory[it]

                    if (obj.name == act.object_name):
                        del player.inventory[it]
                        break
                continue

            if (act.action_type == act.increase_health):
                player.health += act.amount;
                continue

            if (act.action_type == act.reduce_health):
                player.health -= act.amount;
                continue

        outputer.add_char ("health", player.health)
        player.set_title()
        outputer.add_char ("occult", player.title)

        for obj in player.inventory:
            outputer.add_object (obj)

        outputer.add_text (node.text)

        for opt in node.options:
            outputer.add_option(opt.text)

        outputer.flush()

        while True:
            action = inputer.get_action ()

            if (action[0] == "spell"):
                spell = player.spells[action[1]]

                self.node_idx = node.spell_options[spell_name]
                break

            if (action[0] == "option"):
                self.node_idx = node.options[action[1]].node
                break

            if (action[0] == "object"):
                raise ("action: \"object\" not implemented!")
            
            if (action[0] == "help"):
                raise ("action: \"help\" not implemented!")
        return

    def loop(self):
        while self.node_idx != "finish":
            self.inner_loop()
        
        node = self.nodes["finish"]
        self.outputer.add_text(node.text)
        self.outputer.flush()

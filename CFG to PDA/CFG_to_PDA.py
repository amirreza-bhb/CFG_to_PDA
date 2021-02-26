from termcolor2 import colored

"""
    https://github.com/amirreza-bhb
    author : Amirreza behboodi
    termcolored has used just for the beauty 
    you can install it from the terminal using pip : pip install termcolor2
"""

class PDA:
    def __init__(self):
        self.input_symbols = []
        self.stack_symbols = []
        self.transitions = []
        self.production_dictionary = {}
        self.productions_list = []
        self.stack_symbols.append('$')
        self.states = ('q0', 'q1', 'q2')

    # read grammar from file
    def load_Cfg(self):
        path = 'input.txt'
        file = open(path).read()
        print('\nGrammar : ')
        print(file)
        self.productions_list = (file.split("\n"))

    # save productions in better shape and extract Alphabets
    def production(self, prod):
        for rule in prod:
            leftHand = rule.split(' -> ')[0].replace(' ', '')
            rightHand = rule.split(' -> ')[1].split(' | ')
            self.production_dictionary[leftHand] = rightHand
        for value in self.production_dictionary.values():
            for char in value:
                if char == 'e':
                    value.remove(char)
                    value.append('λ')
            for k in value:
                if k.islower():
                    if k in self.input_symbols or k == 'λ':
                        continue
                    else:
                        self.input_symbols.append(k)
                        self.stack_symbols.append(k)

    # if both states in a transition be in states , transition will save in a list
    def add_transition(self, fromState, toState, inputChar, topOfStack, stackPushValue):
        assert fromState in self.states and toState in self.states
        self.transitions.append(
            [fromState, inputChar, topOfStack, stackPushValue, toState])

    # set transitions according to grammar and alphabet
    def set_Pda_transitions(self, production_dict):
        self.add_transition('q0', 'q1', 'λ', 'λ', 'S$')
        for i in production_dict:
            for j in production_dict[i]:
                self.add_transition('q1', 'q1', 'λ', i, j)
        for i in self.input_symbols:
            self.add_transition('q1', 'q1', i, i, 'λ')
        self.add_transition('q1', 'q2', 'λ', '$', '$')

# check if grammar is CFG or not


def isCfg(dict):
    for key in dict:
        if len(key) > 1:
            print('Sorry this is not CFG')
            exit()
    return 1

# print pda in transition display


def pretty_print(list):
    j = 0
    print("║\t\t\t\t\t║")
    for i in list:
        fromState = colored(i[j], color="green")
        toState = colored(i[j+4], color="green")
        print(
            f"║ δ({fromState}, {i[j+1]} , {i[j+2]} ) = ( {i[j+3]} , {toState}) \t\t║")


def main(object):
    object.load_Cfg()
    object.production(object.productions_list)
    assert isCfg(object.production_dictionary)
    object.set_Pda_transitions(object.production_dictionary)
    print('\n╔═══════════════════════════════════════╗')
    print("║ Σ : ", object.input_symbols, '\t\t\t║')
    print("║ Γ : ", object.stack_symbols, '\t\t\t║')
    print("║ Q: ", object.states, '\t\t║')
    print('║\t\t\t\t\t║')
    print("║ Q start : ", object.states[0], '\t\t\t║')
    print("║ Q loop  : ", object.states[1], '\t\t\t║')
    print("║ Q final : ", object.states[2], '\t\t\t║')
    pretty_print(object.transitions)
    print('╚═══════════════════════════════════════╝')


if __name__ == '__main__':
    pda = PDA()
    main(pda)

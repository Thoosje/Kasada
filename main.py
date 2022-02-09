from typing import Any

class Kasada_Dissasambler():
    settings: dict[str, Any] = {
        'R': {
            'x': 4,
            'I': 6,
            'k': 8,
            'C': 10,
            'N': 12,
            'z': 14
        },
        'L': {
            'T': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            'U': 50
        }
    }
    
    instructions: list[dict[str, Any]] = [
        { 'name': 'add', 'opcode': 0 },
        { 'name': 'sub', 'opcode': 1 },
        { 'name': 'mul', 'opcode': 2 },
        { 'name': 'div', 'opcode': 3 },
        { 'name': 'mod', 'opcode': 4 },
        { 'name': 'not', 'opcode': 5 },
        { 'name': 'shift_r', 'opcode': 6 },
        { 'name': 'shift_l', 'opcode': 7 },
        { 'name': 'shift_r_unsigned', 'opcode': 8 },
        { 'name': 'shift_l_unsigned', 'opcode': 9 },
        { 'name': 'bitwise_or', 'opcode': 10 },
        { 'name': 'bitwise_xor', 'opcode': 11 },
        { 'name': 'add_to_stack', 'opcode': 12 },
        { 'name': 'add_bytenode_to_stack', 'opcode': 13 },
        { 'name': 'get_el_from_array', 'opcode': 14 },
        { 'name': 'set_el_in_array', 'opcode': 15 },
        { 'name': 'in', 'opcode': 16 },
        { 'name': 'instanceof', 'opcode': 17 },
        { 'name': 'typeof', 'opcode': 18 },
        { 'name': 'get_property_from_obj', 'opcode': 19 }, # Not sure if this is correct
        { 'name': 'set_property_in_obj', 'opcode': 20 }, # Not sure if this is correct
        { 'name': 'create_empty_obj_on_stack', 'opcode': 21 },
        { 'name': 'create_arr_on_stack', 'opcode': 22 },
        { 'name': 'regex', 'opcode': 23 },
        { 'name': 'add_arr_to_stack', 'opcode': 24 },
        { 'name': 'equal', 'opcode': 25 },
        { 'name': 'strict_equal', 'opcode': 26 },
        { 'name': 'not_equal', 'opcode': 27 },
        { 'name': 'not_strict_equal', 'opcode': 28 },
        { 'name': 'less_than', 'opcode': 29 },
        { 'name': 'greater_than', 'opcode': 30 },
        { 'name': 'less_than_or_equal', 'opcode': 31 },
        { 'name': 'greater_than_or_equal', 'opcode': 32 },
        { 'name': 'change_counter', 'opcode': 33 },
        { 'name': 'jump_if_true', 'opcode': 34 },
        { 'name': 'jump_if_false', 'opcode': 35 },
        { 'name': '?', 'opcode': 36 }, # TODO: What is this?
        { 'name': '?', 'opcode': 37 }, # TODO: What is this?
        { 'name': '?', 'opcode': 38 }, # TODO: What is this?
        { 'name': '?', 'opcode': 39 }, # TODO: What is this?
        { 'name': '?', 'opcode': 40 }, # TODO: What is this?
        { 'name': '?', 'opcode': 41 }, # TODO: What is this?
        { 'name': '?', 'opcode': 42 }, # TODO: What is this?
        { 'name': '?', 'opcode': 43 }, # TODO: What is this?
        { 'name': '?', 'opcode': 44 }, # TODO: What is this?
        { 'name': '?', 'opcode': 45 }, # TODO: What is this?
        { 'name': '?', 'opcode': 46 }, # TODO: What is this?
        { 'name': '?', 'opcode': 47 }, # TODO: What is this?
        { 'name': '?', 'opcode': 48 }, # TODO: What is this?
        { 'name': 'null', 'opcode': 49 },
        { 'name': 'push_inj0_to_stack', 'opcode': 50 },
        { 'name': 'push_inj1_to_stack', 'opcode': 51 },
    ]
        

    def __init__(self, _bytenode: str) -> None:
        self.Bytenode = _bytenode
        
        opcodes = self.convert_bytenode_to_opcode(self.Bytenode)
        print(opcodes)

    def convert_bytenode_to_opcode(self, _bytenode: str) -> list[int]:
        counter: int = 0
        opcode: list[int] = []
        
        print(len(_bytenode))
        while counter < len(_bytenode):
            f: int = 0; c: int = 1
            while True:
                a: int = self.settings['L']['T'].index(_bytenode[counter])
                counter += 1
    
                f += c * (a % self.settings['L']['U'])
                if a < self.settings['L']['U']:
                    opcode.append(0 | f)
                    break
                
                f += self.settings['L']['U'] * c
                c *= (len(self.settings['L']['T']) - self.settings['L']['U'])
            
        return opcode
    
if __name__ == '__main__':
    with open('./bytenode.txt', 'r') as file:
        bytenode = file.read()
        file.close()
    
    Kasada_Dissasambler(bytenode)
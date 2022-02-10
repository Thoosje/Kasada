from typing import Any, Union

from Utils import exceptions as Kasada_Exceptions

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
        { 'name': 'add', 'opcode': 0, 'function': None },
        { 'name': 'sub', 'opcode': 1, 'function': None },
        { 'name': 'mul', 'opcode': 2, 'function': None },
        { 'name': 'div', 'opcode': 3, 'function': None },
        { 'name': 'mod', 'opcode': 4, 'function': None },
        { 'name': 'not', 'opcode': 5, 'function': None },
        { 'name': 'shift_r', 'opcode': 6, 'function': None },
        { 'name': 'shift_l', 'opcode': 7, 'function': None },
        { 'name': 'shift_r_unsigned', 'opcode': 8 , 'function': None},
        { 'name': 'shift_l_unsigned', 'opcode': 9, 'function': None },
        { 'name': 'bitwise_or', 'opcode': 10, 'function': None },
        { 'name': 'bitwise_xor', 'opcode': 1, 'function': None },
        { 'name': 'add_to_stack', 'opcode': 12, 'function': None },
        { 'name': 'add_bytenode_to_stack', 'opcode': 13, 'function': None },
        { 'name': 'get_el_from_array', 'opcode': 14, 'function': None },
        { 'name': 'set_el_in_array', 'opcode': 15, 'function': None },
        { 'name': 'in', 'opcode': 16, 'function': None },
        { 'name': 'instanceof', 'opcode': 17, 'function': None },
        { 'name': 'typeof', 'opcode': 18, 'function': None },
        { 'name': 'get_property_from_obj', 'opcode': 19, 'function': None }, # Not sure if this is correct
        { 'name': 'set_property_in_obj', 'opcode': 20, 'function': None }, # Not sure if this is correct
        { 'name': 'create_empty_obj_on_stack', 'opcode': 21, 'function': None },
        { 'name': 'create_arr_on_stack', 'opcode': 22, 'function': None },
        { 'name': 'regex', 'opcode': 23, 'function': None },
        { 'name': 'add_arr_to_stack', 'opcode': 24, 'function': None },
        { 'name': 'equal', 'opcode': 25, 'function': None },
        { 'name': 'strict_equal', 'opcode': 26, 'function': None },
        { 'name': 'not_equal', 'opcode': 27, 'function': None },
        { 'name': 'not_strict_equal', 'opcode': 28, 'function': None },
        { 'name': 'less_than', 'opcode': 29, 'function': None },
        { 'name': 'greater_than', 'opcode': 30, 'function': None },
        { 'name': 'less_than_or_equal', 'opcode': 31, 'function': None },
        { 'name': 'greater_than_or_equal', 'opcode': 32, 'function': None },
        { 'name': 'change_counter', 'opcode': 33, 'function': None },
        { 'name': 'jump_if_true', 'opcode': 34, 'function': None },
        { 'name': 'jump_if_false', 'opcode': 35, 'function': None },
        { 'name': '?', 'opcode': 36, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 37, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 38, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 39, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 40, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 41, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 42, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 43, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 44, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 45, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 46, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 47, 'function': None }, # TODO: What is this?
        { 'name': '?', 'opcode': 48, 'function': None }, # TODO: What is this?
        { 'name': 'null', 'opcode': 49, 'function': None },
        { 'name': 'push_inj0_to_stack', 'opcode': 50, 'function': None },
        { 'name': 'push_inj1_to_stack', 'opcode': 51, 'function': None },
    ]
        

    def __init__(self, _bytenode: str) -> None:
        self.Bytenode = _bytenode

        self.Stack = [
            1, # Opcode counter
            {
                
            } # Utils funcs
        ]
        
        opcodes = self.convert_bytenode_to_opcode(self.Bytenode)
        print(opcodes)
        
        for i in range(5000):
            print(self.pull_from_stack(opcodes))
    
    def _add_to_counter(self, value: int) -> int:
        orginalValue = self.Stack[0]
        self.Stack[0] += value
        
        return orginalValue
    
    def _get_opcode_data(self, opcode: int) -> dict[str, Any]:
        for instruction in self.instructions:
            if instruction['opcode'] == opcode:
                return instruction
            
        raise Kasada_Exceptions.OpCode_Does_Not_Exist(f'Opcode {opcode} does not exist.')
    
    def _get_from_stack(self, _index: int) -> Any:
        print('Getting value from stack with index: ', _index)
        return self.Stack[_index]
    
    def convert_bytenode_to_opcode(self, _bytenode: str) -> list[int]:
        counter: int = 0
        opcode: list[int] = []

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
    
    def pull_from_stack(self, _opCodeArray: list[int]) -> Union[str, int]:
        r: int = _opCodeArray[self._add_to_counter(1)]
        
        if 1 & r: return r >> 1
        if r == self.settings['R']['x']:
            i: int = _opCodeArray[self._add_to_counter(1)]
            o: int = _opCodeArray[self._add_to_counter(1)]
            e: int = -1 if 2147483648 & i else 1
            u: int = (2146435072 & i) >> 20
            f: int = (1048575 & i) * (2 ** 32) + ( o + (2 ** 32) if o < 0 else o )

            if u == 2047:
                if f:
                    return float('nan')
                else:
                    return 1 / 0 * e
            else:
                if u != 0:
                    f += 2 ** 52
                    return f 
                else:
                    u += 1
                    return e * f * (2 ** (u - 1075))
        
        if r != self.settings['R']['I']: 
            if r == self.settings['R']['k']:
                return True
            elif r == self.settings['R']['C']:
                return False
            
            if r == self.settings['R']['N']:
                return None #null
            else:
                if r != self.settings['R']['z']:
                    return self._get_from_stack(r >> 5) # test dit
                else:
                    return None #void 0 
        
        v: int = 0
        a: int = _opCodeArray[self._add_to_counter(1)]
        c: str = ''
        while v < a:
            s: int = _opCodeArray[self._add_to_counter(1)]
            c += chr(4294967232 & s | 39 * s & 63)
            v += 1
        
        return c
            
if __name__ == '__main__':
    with open('./bytenode.txt', 'r') as file:
        bytenode = file.read()
        file.close()
    
    Kasada_Dissasambler(bytenode)
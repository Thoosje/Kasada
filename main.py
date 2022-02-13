import re
from typing import Any, Union

from Utils import exceptions as Kasada_Exceptions
from Utils.expandable_list import Expandable_List

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
    
    # name: opcode name
    # opcode: opcode id
    # args: args for the opcode. list[tuple(type, required)]
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
        { 'name': 'set_helper_array_el', 'opcode': 36 }, # TODO: What is this?
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

        def return_0_array():
            return [0]
        
        def empty_func():
            pass
        
        self.Stack = [
            1, # Opcode counter
            {
                'u': {}, # Window object
                'a': None,
                'f': Expandable_List(),
                'v': return_0_array,
                'h': return_0_array,
                '$': empty_func
            } # Utils funcs
        ]
        
        opcodes = self.convert_bytenode_to_opcode(self.Bytenode)
        
        self.run_vm(opcodes)
        
    def _add_to_counter(self, value: int) -> int:
        orginalValue = self.Stack[0]
        self.Stack[0] += value
        
        return orginalValue
    
    def _get_opcode_data(self, opcode: int) -> dict[str, Any]:
        for args in self.instructions:
            if args['opcode'] == opcode:
                return args
            
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
    
    def create_data_from_bytenode(self, _opCodeArray: list[int]) -> Union[str, int]:
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
    
    def place_data_on_stack(self, _opCodeArray: list[int], _data: Any) -> None:
        self.Stack[_opCodeArray[self._add_to_counter(1)] >> 5] = _data
    
    def run_vm(self, _opCodeArray: list) -> None:
        while True:
            opCode_data: dict[str, Any] = self._get_opcode_data(_opCodeArray[self._add_to_counter(1)])
            
            if opCode_data['name'] == 'null':
                break

            self.run_instructions(opCode_data['opcode'], _opCodeArray)  
            
    def run_instructions(self, _opCode: int, _opCodeArray: list) -> Any:
        opCode_data: dict[str, Any] = self._get_opcode_data(_opCode)
        print(_opCode)
        match _opCode:
            case 0:
                return self.create_data_from_bytenode(_opCodeArray) + self.create_data_from_bytenode(_opCodeArray)
            case 1:
                return self.create_data_from_bytenode(_opCodeArray) - self.create_data_from_bytenode(_opCodeArray)
            case 2:
                return self.create_data_from_bytenode(_opCodeArray) * self.create_data_from_bytenode(_opCodeArray)
            case 3:
                return self.create_data_from_bytenode(_opCodeArray) / self.create_data_from_bytenode(_opCodeArray)
            case 4:
                return self.create_data_from_bytenode(_opCodeArray) % self.create_data_from_bytenode(_opCodeArray)
            case 5:
                return not self.create_data_from_bytenode(_opCodeArray)
            case 6:
                return self.create_data_from_bytenode(_opCodeArray) >> self.create_data_from_bytenode(_opCodeArray)
            case 7:
                return self.create_data_from_bytenode(_opCodeArray) << self.create_data_from_bytenode(_opCodeArray)
            case 8:
                return self.create_data_from_bytenode(_opCodeArray) >> self.create_data_from_bytenode(_opCodeArray)
            case 9:
                return self.create_data_from_bytenode(_opCodeArray) << self.create_data_from_bytenode(_opCodeArray)
            
            case 36:
                t = self.create_data_from_bytenode(_opCodeArray)
                r = self.create_data_from_bytenode(_opCodeArray)
                print(t, r)
                self.Stack[1]['f'][t] = r # This will throw an out of range error because python lists behave different then js lists.
                print(self.Stack[1]['f'])
                return 'No return data.'
            
        
                
            
if __name__ == '__main__':
    with open('./bytenode.txt', 'r') as file:
        bytenode = file.read()
        file.close()
    
    Kasada_Dissasambler(bytenode)
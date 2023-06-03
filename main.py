from typing import Any, Union
import hashlib

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
    
    # name: opcode name
    # args: amount of objects pulled from stack
    # opcode: opcode id -> Will be automaically set: first element = 0
    # args: args for the opcode. list[tuple(type, required)]
    instructions: list[dict[str, Any]] = [
        {'name': 'mul'},
        {'name': 'equal'},
        {'name': 'less_or_equal'},
        {'name': 'push_empty_array'},
        {'name': 'new_array'},
        {'name': 'greater_than'},
        {'name': 'execute_func_stack_2_param'},
        {'name': 'jump_if_true'},
        {'name': 'execute_func_stack_0_param'},
        {'name': 'logical_not'},
        {'name': 'unsigned_r_shift'},
        {'name': 'strict_not_equal'},
        {'name': 'resave_el'}, # TODO: Check this one more concrete
        {'name': 'XOR'},
        {'name': 'TODO'}, #TODO: Check this one,
        {'name': 'minus'},
        {'name': 'new_func_object'}, # NOTE: This opCode adds void 0 as first argument and creates a new instance of the called function and passes the arguments including the undefined
        {'name': 'TODO'}, # TODO: Check what happens with stack,
        {'name': 'r_shift'},
        {'name': 'execute_func_stack_1_param'},
        {'name': 'regexp'},
        {'name': 'TODO'}, # TODO: Check what happens with stack,
        {'name': 'saved_undefined'}, #TODO: Cehck in what it is saved
        {'name': 'TODO'}, #TODO: Check this one more concrete
        {'name': 'execute_func_stack_3_param'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'greater_or_equal'},
        {'name': 'plus'},
        {'name': 'delete_obj_el'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'smaller_than'},
        {'name': 'l_shift'},
        {'name': 'edit_obj_el_by_key'},
        {'name': 'jump_if_false'},
        {'name': 'typeof'},
        {'name': 'string_to_int'}, # NOTE: If string is not int: Nan
        {'name': 'new_function'}, # TODO: Or end, not sure yet
        {'name': 'copy_array'},
        {'name': 'instanceof'},
        {'name': 'jump_to'},
        {'name': 'resave_el'},
        {'name': 'bitwise_and'},
        {'name': 'bitwise_or'},
        {'name': 'save_empty_obj'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'in_check'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'strict_equal'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'mod'},
        {'name': 'save_el'}, #TODO: Cehck in what it is saved
        {'name': 'divide'},
        {'name': 'save_value_from_key'},
        {'name': 'bitwise_not'},
        {'name': 'TODO'}, # TODO: Check what happens with stack
        {'name': 'not_equal'}
    ]
    
    for idx, x in enumerate(instructions):
        instructions[idx]['opcode'] = idx
    

    def __init__(self, bytecode: str) -> None:        
        self.bytecode = bytecode
        self.bytecodeHash = hashlib.md5(self.bytecode.encode()).hexdigest()
        
        self.Stack = [
            1, # Opcode counter
        ]
        
        opcodes = self.convert_bytecode_to_opcode(self.bytecode)
        
        self.run_dissambler(opcodes)
        
    def _add_to_counter(self, value: int) -> int:
        orginalValue = self.Stack[0]
        self.Stack[0] += value
        
        return orginalValue
    
    def _get_opcode_data(self, opcode: int) -> dict[str, Any]:
        try:
            return self.instructions[opcode]
        except:
            raise Kasada_Exceptions.OpCode_Does_Not_Exist(f'Opcode {opcode} does not exist.')
    
    def _get_from_stack(self, _index: int) -> Any:
        print('Getting value from stack with index: ', _index)
        return self.Stack[_index]
    
    def convert_bytecode_to_opcode(self, _bytecode: str) -> list[int]:
        counter: int = 0
        opcode: list[int] = []

        while counter < len(_bytecode):
            f: int = 0; c: int = 1
            while True:
                a: int = self.settings['L']['T'].index(_bytecode[counter])
                counter += 1
    
                f += c * (a % self.settings['L']['U'])
                if a < self.settings['L']['U']:
                    opcode.append(0 | f)
                    break
                
                f += self.settings['L']['U'] * c
                c *= (len(self.settings['L']['T']) - self.settings['L']['U'])
            
        return opcode
    
    def create_data_from_bytecode(self, _opCodeArray: list[int]) -> Union[str, int]:
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
    
    def run_dissambler(self, _opCodeArray: list) -> None:
        instructions_file = open('kasada_instructions.txt', 'w')
        instructions_file.write(f'# Kasada instructions for: {self.bytecodeHash} #\n')

        while True:
            opCode_data: dict[str, Any] = self._get_opcode_data(_opCodeArray[self._add_to_counter(1)])

            if opCode_data['name'] == 'new_function':
                instructions_file.write(f'''
                    Opcode: {opCode_data["opcode"]}
                    Name: {opCode_data["name"]}
                    Note: End of function
                ''')
                break
            
            
            instructions_file.write(f'''
                Opcode: {opCode_data["opcode"]}
                Name: {opCode_data["name"]}
            ''')
            
        instructions_file.close()
                  
            
if __name__ == '__main__':
    with open('./bytecode.txt', 'r') as file:
        bytecode = file.read()
        file.close()
    
    Kasada_Dissasambler(bytecode)
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

    def __init__(self, _bytenode: str) -> None:
        self.Bytenode = _bytenode
        
        opcodes = self.convert_bytenode_to_opcode(self.Bytenode)
        print(opcodes[144770])

    def convert_bytenode_to_opcode(self, _bytenode: str) -> list[int]: # Not 100% working yet
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
                
                f += self.settings['L']['U'] * c; c *= (len(self.settings['L']['T']) - self.settings['L']['U'])
            
        return opcode
    
if __name__ == '__main__':
    with open('./bytenode.txt', 'r') as file:
        bytenode = file.read()
        Kasada_Dissasambler(bytenode)
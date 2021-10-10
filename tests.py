from object_core import Builder, BaseObject
import os
from sys import modules

class BaseObjectExtended(BaseObject):
    pass

class DataClass(BaseObject):
    pass

builder = Builder(modules[__name__])

if __name__ == '__main__':
    print('\nBeginning tests\n')
    with open(os.path.join('test_json', 'test_basic.json'), 'r') as f:
        print(' === test_basic.json ===\n')
        obj = builder.build(f.read())
        print('obj.dict:\t\t\t', obj.to_dict())
        print('obj.test:\t\t\t', obj.test)
        print('obj.test_dict:\t\t\t', obj.test_dict)
        print('obj.test_dict.key:\t\t', obj.test_dict.key)
        print('obj.test_dict.recursion.depth:\t', obj.test_dict.recursion.depth)
        obj.test_dict.recursion['depth'] = 5
        print('obj.test_dict.recursion.depth2:\t', obj.test_dict.recursion.depth)
        print('obj.dict2:\t\t\t', obj.to_dict())
    print('\n === \n')
    with open(os.path.join('test_json', 'test_extended.json'), 'r') as f:
        print(' === test_extended.json ===\n')
        obj = builder.build(f.read())
        print('Dir:\t\t\t\t', dir())
        print('obj:\t\t\t\t', obj)
        print('obj.dict:\t\t\t', obj.to_dict())
        print('obj.data:\t\t\t', obj.data)
        print('obj.more_data:\t\t\t', obj.more_data)
        print('obj.more_data.dict:\t\t', obj.more_data.to_dict())
        print('obj.more_data.type:\t\t', obj.more_data.type)
        print('obj.more_data.numbers:\t\t', obj.more_data.numbers)
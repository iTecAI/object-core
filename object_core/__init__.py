import json
from sys import modules
import time
import random
import hashlib

def unique_fingerprint(length=0):
    if length < 1:
        return hashlib.sha256(str(time.time()+random.random())).hexdigest()
    h = hashlib.sha256(str(time.time()+random.random()).encode('utf-8')).hexdigest()
    return ''.join([random.choice(h) for i in range(int(length))])

class BaseObject:
    def __init__(self, module, **dct):
        self._module_ = module
        # Initialize default vals
        if '__objectId__' in dct.keys():
            self.id = dct['__objectId__']
        else:
            self.id = unique_fingerprint(16)
        if '__objectType__' in dct.keys():
            self.type = dct['__objectType__']
        else:
            self.type = '__unspecified__'

        # Recursively generate BaseObjects
        for item in dct.keys():
            if type(dct[item]) == dict:
                setattr(self, item, BaseObject.build(self._module_, dct[item]))
            else:
                setattr(self, item, dct[item])
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def to_dict(self):
        ret = {}
        for key in self.__dict__.keys():
            if key == '_module_':
                pass
            elif key == 'type':
                ret['__objectType__'] = self.type
            elif key == 'id':
                ret['__objectId__'] = self.id
            elif isinstance(self.__dict__[key], BaseObject):
                ret[key] = self.__dict__[key].to_dict()
            else:
                ret[key] = self.__dict__[key]
        return ret

    @classmethod
    def build(cls, module, value):
        if type(value) == str:
            dct = json.loads(value)
        elif type(value) == dict:
            dct = value
        else:
            raise ValueError('<value> must be a JSON-encoded string or a dictionary.')
        
        if '__objectType__' in dct.keys():
            if hasattr(module, dct['__objectType__']):
                if issubclass(getattr(module, dct['__objectType__']), BaseObject):
                    return getattr(module, dct['__objectType__'])(module, **dct)
                return cls(module, **dct)
        return cls(module, **dct)

class Builder:
    def __init__(self, module):
        self._module_ = module
    
    def build(self, value):
        return BaseObject.build(self._module_, value)
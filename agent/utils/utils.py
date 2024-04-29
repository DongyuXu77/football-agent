
class Registry(object):
    r""" helper function to registe sub model 
    """

    def __init__(self, name) -> None:
        self._name = name
        self._module_dict = dict()
    
    @property
    def name(self):
        return self._name
    
    @property
    def module_dict(self):
        return self._module_dict
    
    @property
    def module_name(self):
        return list(self._module_dict.keys())
    
    def register(self, cls):
        module_name = cls.__name__
        if module_name in self._module_dict:
            raise KeyError(f'{module_name} is already registered in {self._name}')
        self._module_dict[module_name] = cls
        
        return cls
    
    def get(self, name):
        if name in self._module_dict:
            return self._module_dict[name]
        else:
            raise KeyError(f'{name} is not registered in {self.name}')
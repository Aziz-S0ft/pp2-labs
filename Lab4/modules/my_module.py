class car():
    def __init__(self,name,module):
        self.name=name
        self.module=module
    def info(self):
        print('Name:',self.name,'Module:',self.module)
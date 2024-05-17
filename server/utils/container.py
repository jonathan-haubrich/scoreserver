from subprocess import Popen, PIPE

class Container:
    def __init__(self, id):
        self.id = id

    @staticmethod
    def from_id(id):
        return Container(id)
    
    @staticmethod
    def from_path(path):
        return Container(path)
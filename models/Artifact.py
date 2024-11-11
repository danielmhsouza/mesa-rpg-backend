

class Artifact:
    
    def __init__(self, name: str, desc: str, category: str):
        self._name = name
        self._desc = desc
        self._category = category

    def getName(self) -> str:
        return self._name
   
    def getDesc(self) -> str:
        return self._desc
   
    def getCategory(self) -> str:
        return self._category
    
    def setName(self, name: str):
        self._name = name
   
    def setDesc(self, desc: str):
        self._desc = desc
   
    def setCategory(self, category: str):
        self._category = category
    
   
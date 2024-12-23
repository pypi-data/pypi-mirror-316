class percentOf:
    value=None
    what=None
    of=None
    def __init__(self,what=0,of=100):
        if True not in [isinstance(what,int),isinstance(what,float)]:
            print("What Must be a int or a float")
            return
        self.what=what
        self.of=of
        if isinstance(of,int):
            self.value=(self.what/100)*of
        elif True in [isinstance(of,list),isinstance(of,tuple),isinstance(of,str)]:
            size=len(of)
            percent=int((what/100)*size)
            if percent not in [None,]:
                self.value=of[0:percent]

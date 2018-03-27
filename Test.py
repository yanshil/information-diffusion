class Test(object):
    def __init__(self):
        self.model = None    # Model*
        self.diffusionSize = -1    # int*
        self.diffusionDuration = -1    # int*

    def Simulation(self, Method):    # int method
        pass
    def SampleRole(self, u):    # int u 
        pass
    def SampleT(self, r):    # int r
        pass
    def SampleT(self, user):   # arg: Node*
        pass  # overload?
    def SampleZ(self, r):   # int r 
        pass
    def SampleZ(self, user):   # Node*
        pass
    def TrueSize(self, ):    # 
        pass
    def TrueDuration(self, ):    # 
        pass
    def SizeAndDuration(self, method):    # int method
        pass

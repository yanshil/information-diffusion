class Model(object):
    def __init__(self):
        self.V = 0
        self.V = 0  # number of users
        self.M = 0  # number of posts
        self.S = 0  # number of sourcee posts
        self.roleNum = 0  # number of roles
        self.K = 0  # numebr of features
        self.maxTime = 0  # maximum delay time
        self.tau0 = 0
        self.tau1 = 0
        self.tau2 = 0
        self.tau3 = 0
        self.alpha = 0
        self.beta_0 = 0  # hyper-parameter of lambda  success
        self.beta_1 = 0
        self.gamma_0 = 0  # hyper-parameter of rho  fail
        self.gamma_1 = 0  # hyper-parameter of rho
        self.rho = None  # 1d pointer. role-active prob (Bionomial)
        self.Lambda = None  # 1d pointer. role-delay prob (geometric)
        self.theta = None  # 2d pointer. user-role prob (Multinomial)
        self.mu = None  # 2d pointer.role-feature mean in Gaussian
        self.delta = None  # 2d pointer.role-feature variance in Gaussian

        self.R = None  # 2d pointer.
        self.T = None
        self.Z = None
        self.nur = None  # 2d pointer.
        self.nr = None  # 1d
        self.nu = None  # 1d
        self.nrz = None  # 2d pointer.
        self.sumz_v = None
        self.sumt_v = None  # 2d pointer.
        self.sumt_r = None  # 1d
        self.E = None  # 2d pointer.
        self.nz_t = None  # 2d pointer.
        self.sumz_m = None
        self.sumz_s = None  # 2d pointer.
        self.sum_lambda = None  # 1d
        self.sum_rho = None  # 1d
        self.sum_mu = None  # 2d pointer.
        self.sum_delta = None  # 2d pointer.

        self.nodeList = None  # vector<Node *>
        self.postList = None  # vector<Post *>
        self.userIdMap = {}  # map<int, int>
        self.dataLoader = None  # DataLoader *

    def Init(self, ):
        pass

    def PrintNr(self, ):
        pass

    def SampleRTZ(self, u, v, y, tiu, tiv, sumtv, sumzv):
        pass

    def SampleDiffusion(self, ):
        pass

    def SampleFeature(self, ):
        pass

    def SampleRole(self, u, x, t):
        pass

    def GetOrInsertUserId(self, key):
        pass

    def GetUserId(self, key):
        pass

    def LoadData(self, dataLoader):
        pass

    def GibbsSampling(self, maxIter, BURN_IN, SAMPLE_LAG):
        pass

    def PrintMu(self, ):
        pass

    def PrintRho(self, ):
        pass

    def PrintTheta(self, ):
        pass

    def Save(self, fileDir):
        pass

    def SaveGaussian(self, ):
        pass

    def SaveRho(self, ):
        pass

    def SaveTheta(self, ):
        pass

    def Test(self, ):
        pass

    def RoleLevelTest(self, ):
        pass

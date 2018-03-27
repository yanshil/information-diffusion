from Data       import NodeAttr, Node, PostAttr, Post, DataLoader
from Model      import Model
from Test       import Test
from Analyzer   import Analyzer
from Util       import Util

# -------------1. Params init--------------#
TEST_METHOD = 0
MAX_ITER = 10
ROLE_NUM = 3
TIME_STEP = 3600
MAX_DELAY_TIME = 24
BURN_IN = 5
SAMPLE_LAG = 5
ALPHA = (ROLE_NUM + 0.0) / 50
BETA_0 = 1
BETA_1 = 1
GAMMA_0 = 1
GAMMA_1 = 1

NETWORK_FILE_DIR = ""
DIFFUSION_FILE_DIR = ""
NETWORK_CONSTRAINT_FILE_DIR = ""
PAGE_RANK_FILE_DIR = ""
MODEL_FILE_DIR = "model.txt"
# 这玩意可以写成参数形式

# ------------2. Load Data ----------------#

dataLoader = DataLoader() # 暂时没有参数
dataLoader.TIME_STEP = TIME_STEP
dataLoader.NETWORK_FILE_DIR = NETWORK_FILE_DIR
dataLoader.DIFFUSION_FILE_DIR = DIFFUSION_FILE_DIR
dataLoader.NETWORK_CONSTRAINT_FILE_DIR = NETWORK_CONSTRAINT_FILE_DIR
dataLoader.PAGE_RANK_FILE_DIR = PAGE_RANK_FILE_DIR
dataLoader.LoadData()

model = Model()

model.LoadData(dataLoader)
model.alpha   = ALPHA
model.beta_0  = BETA_0
model.beta_1  = BETA_1
model.gamma_0 = GAMMA_0
model.gamma_1 = GAMMA_1
model.roleNum = ROLE_NUM
model.maxTime = MAX_DELAY_TIME

test = Test()
test.model = model
test.TrueSize()
test.TrueDuration()

if TEST_METHOD == 0 :
    model.GibbsSampling(MAX_ITER, BURN_IN, SAMPLE_LAG) # BURN_IN = 5, SAMPLE_LAG = 5
    model.Save(MODEL_FILE_DIR);

model.Test()
from Data import Node
from Model import Model

from typing import List
import numpy as np


class Test(object):
    def __init__(self):
        self.model = None    # type: Model
        self.diffusionSize = None    # type: List[int]
        self.diffusionDuration = None    # type: List[int]

    def Simulation(self, method):
        """

        :param int method:
        :rtype: int
        :return:
        """

        pass

    def SampleRole(self, u):
        """

        :param int u:
        :rtype: int
        :return:
        """
        rolenum = self.model.roleNum
        p = np.ndarray([rolenum])
        p[0] = self.model.theta[u][0]
        for r in range(1, rolenum):
            p[r] = p[r-1] + self.model.theta[u][r]
        role = np.random.choice(rolenum, size=1, p=p/np.sum(p))
        return role

    def SampleT(self, r):
        """

        :param int | Node r:
        :rtype: int
        :return: None
        """
        if isinstance(r, Node):
            pass
        elif isinstance(r, int):
            t = np.random.geometric(p=self.model)
        pass

    def SampleZ(self, r):
        """

        :param int | Node r:
        :rtype: int
        :return: None
        """
        if isinstance(r, Node):
            pass
        elif isinstance(r, int):
            pass
        pass

    def TrueSize(self, ):
        """

        :rtype: int
        :return:
        """
        pass

    def TrueDuration(self, ):
        """

        :rtype: int
        :return:
        """
        pass

    def SizeAndDuration(self, method):
        """

        :param int method:
        :rtype: int
        :return:
        """
        pass

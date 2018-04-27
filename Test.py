from Data import Node
from Model import model

from typing import List
import numpy as np


class Test(object):
    """

    Attributes:
        model (Model):
        diffusionSize (List[int]):
        diffusionDuration (List[int]):

    """
    def __init__(self):
        self.model = None
        self.diffusionSize = None
        self.diffusionDuration = None

    def SampleRole(self, u):
        """Sample the role of user **u** *w.r.t.* his theta

        Args:
            u (int): index of user whose role is to be sampled

        Returns:
            role (int): role of user **u**

        """
        rolenum = self.model.roleNum
        p = np.array(self.model.theta[u][0:rolenum])
        role = np.random.choice(rolenum, size=1, p=p/np.sum(p))
        return role

    def SampleT(self, r):
        """Sample diffusion delay **T** *w.r.t.* role or user

        Args:
            r (int|Node): role if int, user if node

        Returns:
            t (int): diffusion delay

        """
        t = None
        if isinstance(r, Node):
            pass
        elif isinstance(r, int):
            t = np.random.geometric(p=self.model.Lambda[r])
        return t

    def SampleZ(self, r):
        """

        Args:
            r (int|Node): role if int, user if node

        Returns:
            z (int): 1 if successful, 0 if failed

        """
        z = None
        if isinstance(r, Node):
            pass
        elif isinstance(r, int):
            if np.random.random_sample(1) > self.model.rho[r]:
                z = 0
            else:
                z = 1
        return z


    def Simulation(self, method):
        """

        Args:
            method (int):

        Returns:
            (int):

        """

        pass

    def TrueSize(self, ):
        """

        Returns:
            (int):

        """
        pass

    def TrueDuration(self, ):
        """

        Returns:
            (int):

        """
        pass

    def SizeAndDuration(self, method):
        """

        Args:
            method (int):

        Returns:
            (int):

        """
        pass

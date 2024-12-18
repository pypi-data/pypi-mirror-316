import numpy as np


class ExplicitGeometryMetrics(object):

    def __init__(self, element):
        self.element = element

    def calculateMetrics(self) -> None:
        self.calculateLimits()
        self.calculateCentroid()

    def calculateLimits(self) -> None:
        _min, _max = np.min(np.array(self.element.getNodes()), axis=0), np.max(np.array(self.element.getNodes()), axis=0)
        self.element.setLimits(limits=np.array([_min, _max]))

    def calculateCentroid(self) -> None:
        centroid = np.average(self.element.getNodes(), axis=0)
        self.element.setCentroid(centroid=centroid)

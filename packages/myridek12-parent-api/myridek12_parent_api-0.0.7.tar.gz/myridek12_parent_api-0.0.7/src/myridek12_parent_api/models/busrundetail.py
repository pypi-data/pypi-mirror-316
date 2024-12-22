"""Student Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import BusRunDetail

from typing import Optional

class BusRunDetail(DataModel):
    """Student Model Definition"""
    def __init__(self, busrundetail_resp: BusRunDetail):
        self._directionId                 = busrundetail_resp.directionId
        self._directions                  = busrundetail_resp.directions
        self._distance                    = busrundetail_resp.distance
        self._time                        = busrundetail_resp.time
        self._stopTime                    = busrundetail_resp.stopTime
        self._stopId                      = busrundetail_resp.stopId
        self._runStopId                   = busrundetail_resp.runStopId
        self._runStopSeq                  = busrundetail_resp.runStopSeq
        self._directionSeq                = busrundetail_resp.directionSeq

    @property
    def directionId                 (self) -> int:
        """Property Definition"""
        return self._directionId
    @property
    def directions                  (self) -> str:
        """Property Definition"""
        return self._directions
    @property
    def distance                    (self) -> float:
        """Property Definition"""
        return self._distance
    @property
    def time                        (self) -> float:
        """Property Definition"""
        return self._time
    @property
    def stopTime                    (self) -> str:
        """Property Definition"""
        return self._stopTime
    @property
    def stopId                      (self) -> int:
        """Property Definition"""
        return self._stopId
    @property
    def runStopId                   (self) -> int:
        """Property Definition"""
        return self._runStopId
    @property
    def runStopSeq                  (self) -> int:
        """Property Definition"""
        return self._runStopSeq  
    @property
    def directionSeq                  (self) -> int:
        """Property Definition"""
        return self._directionSeq 
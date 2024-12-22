"""Student Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import BusRunDetail

from typing import Optional

class BusRunDetail(DataModel):
    """Student Model Definition"""
    def __init__(self, busrundetail_resp: BusRunDetail):
        self._directionId                 = busrundetail_resp._directionId
        self._directions                  = busrundetail_resp._directions
        self._distance                    = busrundetail_resp._distance
        self._time                        = busrundetail_resp._time
        self._directionGeomLine           = busrundetail_resp._directionGeomLine
        self._stopTime                    = busrundetail_resp._stopTime
        self._stopId                      = busrundetail_resp._stopId
        self._runStopId                   = busrundetail_resp._runStopId
        self._runStopSeq                  = busrundetail_resp._runStopSeq
        self._directionSeq                = busrundetail_resp._directionSeq

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
    def directionGeomLine           (self) -> str:
        """Property Definition"""
        return self._directionGeomLine
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
    def directionpSeq                  (self) -> int:
        """Property Definition"""
        return self._directionSeq 
"""BusStop Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import BusStop
from typing import Optional

class BusStop(DataModel):
    """BusStop Model Definition"""
    def __init__(self, busstop_resp: BusStop):
        self._stopAddress                 = busstop_resp.stopAddress
        self._stopCity                    = busstop_resp.stopCity
        self._stopState                   = busstop_resp.stopState
        self._stopZip                     = busstop_resp.stopZip
        self._actionType                  = busstop_resp.actionType
        self._stopDescription             = busstop_resp.stopDescription
        self._stopAddressFull             = busstop_resp.stopAddressFull
        self._stopTime                    = busstop_resp.stopTime
        self._stopTimeShifted             = busstop_resp.stopTimeShifted
        self._locationTypeCode            = busstop_resp.locationTypeCode
        self._locationId                  = busstop_resp.locationId
        self._locationName                = busstop_resp.locationName
        self._stopId                      = busstop_resp.stopId
        self._stopLat                     = busstop_resp.stopLat
        self._stopLong                    = busstop_resp.stopLong
        self._timeZoneString              = busstop_resp.timeZoneString
        self._seq                         = busstop_resp.seq
        self._etaMinutes                  = busstop_resp.etaMinutes

    @property
    def stopAddress                 (self) -> str:
        """Property Definition"""
        return self._stopAddress
    @property
    def stopCity                    (self) -> str:
        """Property Definition"""
        return self._stopCity
    @property
    def stopState                   (self) -> str:
        """Property Definition"""
        return self._stopState
    @property
    def stopZip                     (self) -> str:
        """Property Definition"""
        return self._stopZip
    @property
    def actionType                  (self) -> str:
        """Property Definition"""
        return self._actionType
    @property
    def stopDescription             (self) -> Optional[str]:
        """Property Definition"""
        return self._stopDescription
    @property
    def stopAddressFull             (self) -> str:
        """Property Definition"""
        return self._stopAddressFull
    @property
    def stopTime                    (self) -> str:
        """Property Definition"""
        return self._stopTime
    @property
    def stopTimeShifted             (self) -> str:
        """Property Definition"""
        return self._stopTimeShifted
    @property
    def locationTypeCode            (self) -> Optional[str]:
        """Property Definition"""
        return self._locationTypeCode
    @property
    def locationId                  (self) -> Optional[int]:
        """Property Definition"""
        return self._locationId
    @property
    def locationName                (self) -> str:
        """Property Definition"""
        return self._locationName
    @property
    def stopId                      (self) -> int:
        """Property Definition"""
        return self._stopId
    @property
    def stopLat                     (self) -> float:
        """Property Definition"""
        return self._stopLat
    @property
    def stopLong                    (self) -> float:
        """Property Definition"""
        return self._stopLong
    @property
    def timeZoneString              (self) -> str:
        """Property Definition"""
        return self._timeZoneString
    @property
    def seq                         (self) -> Optional[int]:
        """Property Definition"""
        return self._seq
    @property
    def etaMinutes                  (self) -> int:
        """Property Definition"""
        return self._etaMinutes
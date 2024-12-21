"""BusStop Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import BusStop
from typing import Optional

class BusStop(DataModel):
    """BusStop Model Definition"""
    def __init__(self, busstop_resp: BusStop):
        self._stopAddress                 = busstop_resp._stopAddress
        self._stopCity                    = busstop_resp._stopCity
        self._stopState                   = busstop_resp._stopState
        self._stopZip                     = busstop_resp._stopZip
        self._actionType                  = busstop_resp._actionType
        self._stopDescription             = busstop_resp._stopDescription
        self._stopAddressFull             = busstop_resp._stopAddressFull
        self._stopTime                    = busstop_resp._stopTime
        self._stopTimeShifted             = busstop_resp._stopTimeShifted
        self._locationTypeCode            = busstop_resp._locationTypeCode
        self._locationId                  = busstop_resp._locationId
        self._locationName                = busstop_resp._locationName
        self._stopId                      = busstop_resp._stopId
        self._stopLat                     = busstop_resp._stopLat
        self._stopLong                    = busstop_resp._stopLong
        self._timeZoneString              = busstop_resp._timeZoneString
        self._seq                         = busstop_resp._seq
        self._etaMinutes                  = busstop_resp._etaMinutes

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
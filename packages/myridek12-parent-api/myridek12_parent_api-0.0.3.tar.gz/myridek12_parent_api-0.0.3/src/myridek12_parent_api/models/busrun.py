"""BusRun Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import BusRun
from myridek12_parent_api.models.busrundetail import BusRunDetail
from myridek12_parent_api.models.busstop import BusStop
from typing import Optional

class BusRun(DataModel):
    """Student Model Definition"""
    def __init__(self, busrun_resp: BusRun):
        self._runName              = busrun_resp._runName
        self._visibleRunName       = busrun_resp._visibleRunName
        self._runId                = busrun_resp._runId
        self._isAdvanced           = busrun_resp._isAdvanced
        self._runDescription       = busrun_resp._runDescription
        self._effectiveDateFrom    = busrun_resp._effectiveDateFrom
        self._effectiveDateTo      = busrun_resp._effectiveDateTo
        self._runningDays          = busrun_resp._runningDays
        self._days                 = busrun_resp._days
        self._busNumber            = busrun_resp._busNumber
        self._rolloutBusNumber     = busrun_resp._rolloutBusNumber
        self._assetUniqueId        = busrun_resp._assetUniqueId
        self._activeVehicle        = busrun_resp._activeVehicle
        self._driverName           = busrun_resp._driverName
        self._rolloutDriverName    = busrun_resp._rolloutDriverName
        self._isCurrentRun         = busrun_resp._isCurrentRun
        self._runTileHeaderText    = busrun_resp._runTileHeaderText
        self._newRunTileHeaderText = busrun_resp._newRunTileHeaderText
        self._timeZoneString       = busrun_resp._timeZoneString
        self._runType              = busrun_resp._runType
        self._tripUniqueId         = busrun_resp._tripUniqueId
        self._studentId            = busrun_resp._studentId
        self._runDetail            = busrun_resp._runDetail
        self._showStopsTimes       = busrun_resp._showStopsTimes
        self._stopsInfo            = busrun_resp._stopsInfo
        self._vehicleStatus        = busrun_resp._vehicleStatus

    @property
    def runName(self) -> str:
        """Property Definition"""
        return self._runName
    @property
    def visibleRunName(self) -> str:
        """Property Definition"""
        return self._visibleRunName
    @property
    def runId(self) -> int:
        """Property Definition"""
        return self._runId
    @property
    def isAdvanced(self) -> bool:
        """Property Definition"""
        return self._isAdvanced
    @property
    def runDescription(self) -> Optional[str]:
        """PropertyDefinition"""
        return self._runDescription
    @property
    def effectiveDateFrom(self) -> str:
        """PropertyDefinition"""
        return self._effectiveDateFrom
    @property
    def effectiveDateTo(self) -> str:
        """PropertyDefinition"""
        return self._effectiveDateTo
    @property
    def runningDats(self) -> list[str]:
        """PropertyDefinition"""
        return self._runningDays
    @property
    def days(self) -> Optional[str]:
        """PropertyDefinition"""
        return self._days
    @property
    def busNumber(self) -> str:
        """PropertyDefinition"""
        return self._busNumber
    @property
    def rolloutBusNumber(self) -> str:
        """PropertyDefinition"""
        return self._rolloutBusNumber
    @property
    def assetUniqueId(self) -> str:
        """PropertyDefinition"""
        return self._assetUniqueId
    @property
    def activeVehicle(self) -> str:
        """PropertyDefinition"""
        return self._activeVehicle
    @property
    def driverName(self) -> str:
        """PropertyDefinition"""
        return self._driverName
    @property
    def rolloutDriverName(self) -> str:
        """PropertyDefinition"""
        return self._rolloutDriverName
    @property
    def isCurrentRun(self) -> bool:
        """PropertyDefinition"""
        return self._isCurrentRun
    @property
    def runTileHeaderText(self) -> Optional[str]:
        """PropertyDefinition"""
        return self._runTileHeaderText
    @property
    def newRunTileHeaderText(self) -> Optional[str]:
        """PropertyDefinition"""
        return self._newRunTileHeaderText
    @property
    def timeZoneString(self) -> str:
        """PropertyDefinition"""
        return self._timeZoneString
    @property
    def runType(self) -> int:
        """PropertyDefinition"""
        return self._runType
    @property
    def tripUniqueId(self) -> str:
        """PropertyDefinition"""
        return self._tripUniqueId
    @property
    def studentId(self) -> int:
        """PropertyDefinition"""
        return self._studentId
    @property
    def runDetail(self) -> list[BusRunDetail]:
        """PropertyDefinition"""
        return [BusRunDetail(rundetail) for rundetail in self._runDetail]
    @property
    def showStopsTimes(self) -> Optional[bool]:
        """PropertyDefinition"""
        return self._showStopsTimes
    @property
    def stopsInfo(self) -> list[BusStop]:
        """PropertyDefinition"""
        return [BusStop(stopinfo) for stopinfo in self._stopsInfo]
    @property
    def vehicleStatus(self) -> int:
        """PropertyDefinition"""
        return self._vehicleStatus
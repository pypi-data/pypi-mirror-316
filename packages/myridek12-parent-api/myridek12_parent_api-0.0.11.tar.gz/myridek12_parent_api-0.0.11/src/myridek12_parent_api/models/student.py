"""Student Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import StudentResponse
from myridek12_parent_api.models.busrun import BusRun
from myridek12_parent_api.models.customfield import CustomField
from myridek12_parent_api.models.address import Address
from typing import Optional

class Student(DataModel):
    """Student Model Definition"""
    def __init__(self, student_resp: StudentResponse):
        self._studentId                   = student_resp.studentId
        self._firstName                   = student_resp.firstName
        self._lastName                    = student_resp.lastName
        self._gradeName                   = student_resp.gradeName
        self._locationname                = student_resp.locationName
        self._isTransportationInfoVisible = student_resp.isTransportationInfoVisible
        self._runInfo                     = student_resp.runInfo
        self._customFields                = student_resp.customFields
        self._homeAddress                 = student_resp.homeAddress
        self._lastScan                    = student_resp.lastScan
        self._hasRunToday                 = student_resp.hasRunToday
        self._hasRunAssigned              = student_resp.hasRunAssigned

    @property
    def studentId(self) -> Optional[int]:
        """Property Definition"""
        return self._studentId
    
    @property
    def firstName(self) -> str:
        """Property Definition"""
        return self._firstName

    @property
    def lastName(self) -> str:
        """Property Definition"""
        return self._lastName
    
    @property
    def gradeName(self) -> str:
        """Property Definition"""
        return self._gradeName
    
    @property
    def locationName(self) -> str:
        """Property Definition"""
        return self._locationname
    
    @property
    def isTransportationInfoVisible(self) -> bool:
        """Property Definition"""
        return self._isTransportationInfoVisible
    
    @property
    def runInfo(self) -> list[BusRun]:
        """Property Definition"""
        return [BusRun(run) for run in self._runInfo]
    
    @property
    def customFields(self) -> list[CustomField]:
        """Property Definition"""
        return [CustomField(customfield) for customfield in self._customFields]
    
    @property
    def homeAddress(self) -> Address:
        """Property Definition"""
        return Address(self._homeAddress)
    
    @property
    def lastScan(self) -> Optional[str]:
        """Property Definition"""
        return self._lastScan
    
    @property
    def hasRunToday(self) -> bool:
        """Property Definition"""
        return self._hasRunToday
    
    @property
    def hasRunAssigned(self) -> Optional[bool]:
        """Property Definition"""
        return self._hasRunAssigned
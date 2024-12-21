"""Base Model Definition."""
from typing import Optional
from pydantic import BaseModel, Field

class BusRunDetail(BaseModel):
    """BusRunDetail Definition."""
    class Config:
        exclude = ['distanceToVehicle','distanceToStartPoint','distanceToEndPoint','tripGroupId']
    directionId                 : int
    directions                  : str
    distance                    : float
    time                        : float
    directionGeomLine           : str
    stopTime                    : str
    stopId                      : int
    runStopId                   : int
    runStopSeq                  : int
    directionSeq                : int

class BusStop(BaseModel):
    """BusStop Definition"""
    class Config:
        exclude = []
    stopAddress                 : str
    stopCity                    : str
    stopState                   : str
    stopZip                     : str
    actionType                  : str
    stopDescription             : Optional[str]
    stopAddressFull             : str
    stopTime                    : str
    stopTimeShifted             : str
    locationTypeCode            : Optional[str]
    locationId                  : Optional[int]
    locationName                : str
    stopId                      : int
    stopLat                     : float
    stopLong                    : float
    timeZoneString              : str
    seq                         : Optional[int]
    etaMinutes                  : int

class BusRun(BaseModel):
    """BusRun Definition."""
    class Config:
        exclude= ['routePackage','runpath','cachedMapColor','cachedExtent']
    runName                     : Optional[str]
    visibleRunName              : str
    runId                       : int
    isAdvanced                  : bool
    runDescription              : Optional[str]
    effectiveDateFrom           : str
    effectiveDateTo             : str
    runningDays                 : list[str]
    days                        : Optional[str]
    busNumber                   : str
    rolloutBusNumber            : str
    assetUniqueId               : str
    activeVehicle               : str
    driverName                  : str
    rolloutDriverName           : str
    isCurrentRun                : bool
    runTileHeaderText           : Optional[str]
    newRunTileHeaderText        : Optional[str]
    timeZoneString              : str
    runType                     : int
    tripUniqueId                : str
    studentId                   : int
    runDetail                   : list[BusRunDetail]
    showStopsTimes              : Optional[bool]
    stopsInfo                   : list[BusStop]
    vehicleStatus               : int

class CustomField(BaseModel):
    """CustomFields Definition"""
    class Config:
        exclude = []
    entityName                  : str
    entityKey                   : int
    attributeName               : str
    attributeValue              : str
    attributeSeq                : int
    attributeType               : str
    entityAttributeId           : int
    attributeTypeCode           : int
    isConfidential              : bool

class Address(BaseModel):
    """Address Definition"""
    class Config:
        exclude = []
    addrLine1                   : str
    addrLine2                   : str
    city                        : str
    state                       : str
    zip                         : str
    country                     : Optional[str] = None
    latitude                    : float
    longitude                   : float

class StudentResponse(BaseModel):
    """MyStudents Response Definition."""
    class Config:
        exclude= ['uniqueId','programName','photo','isShared','studentOptOutStartDate','StudentOptOutEndDate','studentOptOutStatusCode','studentOptOutStatusDescription','newStudentShareFrom','ruleLookupSessionKey','studentOptOuts','optOutIndefinitely','isOptedOut','optOutDateInvalid']
    studentId                   : Optional[int]
    firstName                   : str
    lastName                    : str
    gradeName                   : str
    locationName                : str
    isTransportationInfoVisible : bool
    runInfo                     : list[BusRun]
    customFields                : list[CustomField]
    homeAddress                 : Address
    lastScan                    : Optional[str] = None
    hasRunToday                 : bool
    hasRunAssigned              : Optional[bool] = None
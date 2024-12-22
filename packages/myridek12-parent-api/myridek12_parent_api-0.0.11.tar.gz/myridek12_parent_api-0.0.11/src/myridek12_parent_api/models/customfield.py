"""Custom Field Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import CustomField
from typing import Optional

class CustomField(DataModel):
    """Custom Field Model Definition"""
    def __init__(self, customfield_resp: CustomField):
        self._entityName                  = customfield_resp.entityName
        self._entityKey                   = customfield_resp.entityKey
        self._attributeName               = customfield_resp.attributeName
        self._attributeValue              = customfield_resp.attributeValue
        self._attributeSeq                = customfield_resp.attributeSeq
        self._attributeType               = customfield_resp.attributeType
        self._entityAttributeId           = customfield_resp.entityAttributeId
        self._attributeTypeCode           = customfield_resp.attributeTypeCode
        self._isConfidential              = customfield_resp.isConfidential

    @property
    def entityName                  (self) -> Optional[str]:
        """Property Definition"""
        return self._entityName
    @property
    def entityKey                   (self) -> int:
        """Property Definition"""
        return self._entityKey
    @property
    def attributeName               (self) -> str:
        """Property Definition"""
        return self._attributeName
    @property
    def attributeValue              (self) -> str:
        """Property Definition"""
        return self._attributeValue
    @property
    def attributeSeq                (self) -> int:
        """Property Definition"""
        return self._attributeSeq
    @property
    def attributeType               (self) -> str:
        """Property Definition"""
        return self._attributeType
    @property
    def entityAttributeId           (self) -> int:
        """Property Definition"""
        return self._entityAttributeId
    @property
    def attributeTypeCode           (self) -> int:
        """Property Definition"""
        return self._attributeTypeCode
    @property
    def isConfidential              (self) -> bool:
        """Property Definition"""
        return self._isConfidential
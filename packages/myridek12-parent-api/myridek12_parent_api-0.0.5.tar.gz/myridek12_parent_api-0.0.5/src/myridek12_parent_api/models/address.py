"""Address Model Definition"""
from myridek12_parent_api.base import DataModel
from myridek12_parent_api.myridek12_api_client import Address
from typing import Optional

class Address(DataModel):
    """Address Model Definition"""
    def __init__(self, address_resp: Address):
        self._addrLine1   = address_resp.addrLine1
        self._addrLine2   = address_resp.addrLine2
        self._city        = address_resp.city
        self._state       = address_resp.state
        self._zip         = address_resp.zip
        self._country     = address_resp.country
        self._latitude    = address_resp.latitude
        self._longitude   = address_resp.longitude

    @property
    def addrLine1(self) -> str:
        """Property Definition"""
        return self._addrLine1
    
    @property
    def addrLine2(self) -> str:
        """Property Definition"""
        return self._addrLine2
    
    @property
    def city(self) -> str:
        """Property Definition"""
        return self._city
    
    @property
    def state(self) -> str:
        """Property Definition"""
        return self._state
    
    @property
    def zip(self) -> str:
        """Property Definition"""
        return self._zip
    
    @property
    def country(self) -> str:
        """Property Definition"""
        return self._country
    
    @property
    def latitude(self) -> float:
        """Property Definition"""
        return self._latitude
    
    @property
    def longitude(self) -> float:
        """Property Definition"""
        return self._longitude
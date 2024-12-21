"""Base MyRideK12 Class."""
import logging

from .models.student import Student
from .myridek12_api_client import MyRideK12ApiClient

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class MyRideK12():
    """Define MyRideK12s Class."""
    def __init__(
        self,
        username,
        password,
        debug = False,
    ):
        self._api_client = MyRideK12ApiClient(username,password,debug)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)
        
    async def get_token(self) -> str:
        """Get API Token from MyRideK12 """
        token = await self._api_client.get_token()
        return token
    
    async def get_students(self, token) -> list[Student]:
        """Get Students from MyRideK12 """
        studentsresp = await self._api_client.get_students(token)
        students = [Student(response) for response in studentsresp]
        return students
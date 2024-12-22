from typing import Any, Union

from syncmaster_commons.abstract.baseclass import (SMBaseClass,
                                                   ThirdPartyPayload)
from syncmaster_commons.gupshup.request_payload import \
    _AgentRequestPayloadGupshup


class AgentRequestPayload(SMBaseClass):
    """
    AgentRequestPayload class for handling agent request payloads.
    Attributes:
        agent_request_payload (Union[_AgentRequestPayloadGupshup]): The payload data for the agent request.
    Methods:
        from_dict(cls, request_payload: dict, client: str = None) -> "AgentRequestPayload":
            Creates an AgentRequestPayload object from a dictionary.
                request_payload (dict): The dictionary containing the payload data.
                client (str, optional): The client type. Defaults to None.
            Raises:
                ValueError: If the client is not supported.
    """
    payload: Union[ThirdPartyPayload,Any]

    @property
    def org_id(self) -> int:
        """
        Returns the organization id.
        """
        return self.payload.org_id
    
    @property
    def user_id(self) -> str:
        """
        Returns the user id.
        """
        return self.payload.user_id
    
    @property
    def task_id(self) -> int:
        """
        Returns the task id.
        """
        return self.payload.task_id


    @classmethod
    def from_dict(cls,request_payload: dict, client:str = None) -> "AgentRequestPayload":
        """
        Creates a AgentRequestPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            AgentRequestPayload: The AgentRequestPayload object created from the dictionary.
        """
        app_name = request_payload.get("app_name", None)
        if client == "gupshup" or app_name == "gupshup":
            payload = _AgentRequestPayloadGupshup.from_dict(request_payload) 
        else:
            raise ValueError(f"Client {client} is not supported.")
        return cls(
            payload=payload,
        )

    
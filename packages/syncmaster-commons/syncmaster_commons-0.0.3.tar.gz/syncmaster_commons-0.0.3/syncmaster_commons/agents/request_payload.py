from typing import Union

from syncmaster_commons.abstract.baseclass import SMBaseClass
from syncmaster_commons.gupshup.request_payload import \
    _AgentRequestPayloadGupshup


class AgentRequestPayload(SMBaseClass):
    """
    AgentRequestPayload is a pydantic model for the agent request payload.

    """
    agent_request_payload: Union[_AgentRequestPayloadGupshup]


    @classmethod
    def from_dict(cls, client, request_payload: dict) -> "AgentRequestPayload":
        """
        Creates a AgentRequestPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            AgentRequestPayload: The AgentRequestPayload object created from the dictionary.
        """
        if client == "gupshup":
            agent_request_payload = _AgentRequestPayloadGupshup.from_dict(request_payload) 
        else:
            raise ValueError(f"Client {client} is not supported.")
        return cls(
            agent_request_payload=agent_request_payload,
        )

    
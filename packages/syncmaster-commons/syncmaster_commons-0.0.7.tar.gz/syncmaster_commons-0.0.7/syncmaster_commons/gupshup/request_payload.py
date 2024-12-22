from abstract.baseclass import ThirdPartyPayload

from syncmaster_commons.gupshup.incoming_payloads import IncomingPayLoad


class _AgentRequestPayloadGupshup(ThirdPartyPayload):
    """
    _AgentRequestPayloadGupshup is a class that represents a request payload for the Gupshup agent.
    Attributes:
        _incoming_payload (IncomingPayLoad): The incoming payload object.
    Properties:
        app_name (str): Returns the name of the application, which is 'gupshup'.
        _payload_type (str): Returns the type of the payload from the incoming payload.
        payload (dict): Returns the payload as a dictionary with an added 'payload_type' key.
    Methods:
        from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
            Creates an _AgentRequestPayloadGupshup object from a dictionary.
                _AgentRequestPayloadGupshup: The _AgentRequestPayloadGupshup object created from the dictionary.
    """  
    _incoming_payload: IncomingPayLoad
    
    @property
    def app_name(self) -> str:
        return 'gupshup'
    
    @property
    def _payload_type(self) -> str:
        return self._incoming_payload.payload.payload.payload_type
    
    @property
    def payload(self) -> dict:
        payload = self._incoming_payload.payload.payload.payload
        output_dict = payload.to_dict() 
        output_dict["payload_type"] = self._payload_type
        return output_dict
        


    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
        """
        Creates a AgentRequestPayload object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            AgentRequestPayload: The AgentRequestPayload object created from the dictionary.
        """
        return cls(
            _incoming_payload=payload_dict["incoming_payload"],
            task_id=payload_dict["task_id"],
            user_id=payload_dict["user_id"],
            org_id=payload_dict["org_id"],
        )
    

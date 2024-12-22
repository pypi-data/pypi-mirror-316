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
        """
        Returns the name of the application.

        :return: The string 'gupshup'.
        :rtype: str
        """
        return 'gupshup'
    
    @property
    def _payload_type(self) -> str:
        return self._incoming_payload.payload.payload.payload_type
    
    @property
    def _payload(self) -> dict:
        """
        Constructs and returns the payload dictionary.
        This method retrieves the payload from the incoming payload object,
        converts it to a dictionary, and adds the payload type to the dictionary.
        Returns:
            dict: The payload dictionary with an added payload type.
        """
       
        payload = self._incoming_payload.payload.payload.payload
        output_dict = payload.to_dict() 
        output_dict["payload_type"] = self._payload_type
        return output_dict
    
    @property
    def payload(self) -> dict:
        """
        Generates the payload dictionary based on the payload type.

        Returns:
            dict: The payload dictionary.

        Raises:
            NotImplementedError: If the payload type is not supported.
        """
        if self._payload_type == "text":
            #payload["messages"] = ("user", payload["messages"])
            self._payload["messages"] = ("user", self._payload["text"])
        else:
            raise NotImplementedError(f"Payload type '{self._payload_type}' is not supported.")
        return self._payload    
        


    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
        """
        Creates an instance of _AgentRequestPayloadGupshup from a dictionary.
        Args:
            cls: The class itself.
            payload_dict (dict): A dictionary containing the payload data.
        Returns:
            _AgentRequestPayloadGupshup: An instance of the class populated with data from the dictionary.
        Raises:
            KeyError: If 'task_id', 'user_id', or 'org_id' keys are missing in the payload_dict.
        """
        
        _incoming_payload = IncomingPayLoad.from_dict(payload_dict["incoming_payload"])
        if payload_dict.get("user_id", None) is None:
            payload_dict["user_id"] = _incoming_payload.payload.payload.sender.phone
        return cls(
            _incoming_payload=_incoming_payload,
            task_id=payload_dict["task_id"],
            user_id=payload_dict["user_id"],
            org_id=payload_dict["org_id"],
        )
    

from typing import override

from syncmaster_commons.abstract.baseclass import \
    ThirdPartyPayloadConsumedByAgent
from syncmaster_commons.gupshup.incoming_payloads import GupshupIncomingPayLoad


class _AgentRequestPayloadGupshup(ThirdPartyPayloadConsumedByAgent):
    """
    _AgentRequestPayloadGupshup is a class that represents the payload consumed by an agent from Gupshup.
    Attributes:
        _incoming_payload (GupshupIncomingPayLoad): The incoming payload from Gupshup.
    Properties:
        app_name (str): Returns the name of the application, which is 'gupshup'.
        _payload_type (str): Returns the type of the payload.
        payload (dict): Constructs and returns the payload dictionary with an added payload type.
    Methods:
        from_dict(cls, payload_dict: dict) -> "_AgentRequestPayloadGupshup":
  """
    _incoming_payload: GupshupIncomingPayLoad
    
    @property
    def app_name(self) -> str:
        """
        Returns the name of the application.

        :return: The string 'gupshup'.
        :rtype: str
        """
        return self._incoming_payload.app_name
    
    @property
    def _payload_type(self) -> str:
        return self._incoming_payload.payload.payload.payload_type
    
    @property
    def payload(self) -> dict:
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
        if self._payload_type == "text":
            output_dict["messages"] = ("user", output_dict["text"])
        else:
            raise NotImplementedError(f"Payload type '{self._payload_type}' is not supported.")    
        return output_dict
    
    @override
    def to_dict(self):
        """
        Return a dictionary representation of the object.

        Calls the superclass's to_dict() method to get the base dictionary and
        then includes the "incoming_payload" key for additional data.

        Returns:
            dict: The dictionary with updated "incoming_payload" information.
        """
        og_dict =  super().to_dict()
        og_dict["incoming_payload"] = self._incoming_payload.to_dict()
        return og_dict



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
        
        _incoming_payload = GupshupIncomingPayLoad.from_dict(payload_dict["incoming_payload"])
        if payload_dict.get("user_id", None) is None:
            payload_dict["user_id"] = _incoming_payload.payload.payload.sender.phone
        return cls(
            _incoming_payload=_incoming_payload,
            task_id=payload_dict["task_id"],
            org_name=payload_dict["org_name"],
            user_id=payload_dict["user_id"],
            org_id=payload_dict["org_id"],
        )
    

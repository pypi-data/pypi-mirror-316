from abstract.baseclass import ThirdPartyPayload


class _AgentRequestPayloadGupshup(ThirdPartyPayload):
    """
    AgentRequestPayload is a pydantic model for the agent request payload.

    """    
    incoming_payload: dict
    task_id: int
    user_id: str
    org_id: int

    @property
    def app_name(self) -> str:
        return 'gupshup'
    


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
            incoming_payload=payload_dict["incoming_payload"],
            task_id=payload_dict["task_id"],
            user_id=payload_dict["user_id"],
            org_id=payload_dict["org_id"],
        )
    

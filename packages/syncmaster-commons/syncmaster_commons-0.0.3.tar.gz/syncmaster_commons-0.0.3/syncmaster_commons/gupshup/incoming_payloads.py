from typing import Optional, Union

from abstract.baseclass import SMBaseClass
from pydantic import Field


class _ImagePayLoad(SMBaseClass):
    """_ImagePayLoad is a class responsible handling image payloads for the Gupshup API."""

    url: str
    caption: Optional[str] = None
    contenType: str
    urlExpiry: str
    is_expired: bool = False

    @classmethod
    def from_dict(cls, image_dict: dict) -> "_ImagePayLoad":
        """
        Creates a _ImagePayLoad object from a dictionary.
        Args:
            image_dict (dict): The dictionary containing the image data.
        Returns:
            _ImagePayLoad: The _ImagePayLoad object created from the dictionary.
        """
        return cls(
            url=image_dict["url"],
            caption=image_dict.get("caption"),
            contenType=image_dict["contenType"],
            urlExpiry=image_dict["urlExpiry"],
            is_expired=image_dict.get("is_expired", False),
        )


class _TextPayLoad(SMBaseClass):
    """_TextPayLoad is a class responsible handling text payloads for the Gupshup API."""

    text: str

    @classmethod
    def from_dict(cls, text_dict: dict) -> "_TextPayLoad":
        """
        Creates a _TextPayLoad object from a dictionary.
        Args:
            text_dict (dict): The dictionary containing the text data.
        Returns:
            _TextPayLoad: The _TextPayLoad object created from the dictionary.
        """
        return cls(text=text_dict["text"])


class _Sender(SMBaseClass):
    """_Sender is a class responsible for handling the sender details for the Gupshup API."""

    phone: str
    name: str
    country_code: str
    dial_code: str

    @classmethod
    def from_dict(cls, sender_dict: dict) -> "_Sender":
        """
        Creates a _Sender object from a dictionary.
        Args:
            sender_dict (dict): The dictionary containing the sender data.
        Returns:
            _Sender: The _Sender object created from the dictionary.
        """
        return cls(
            phone=sender_dict["phone"],
            name=sender_dict["name"],
            country_code=sender_dict["country_code"],
            dial_code=sender_dict["dial_code"],
        )


class _MessagePayLoad(SMBaseClass):
    """
    _PayLoad class represents a payload structure for the CRM assistant.
    Attributes:
        id (str): Unique identifier for the payload.
        source (str): Source of the payload.
        payload (Union[_ImagePayLoad, _TextPayLoad]): The actual payload which can be either an image or text.
        sender (_Sender): The sender information of the payload.
    """

    id: str
    source: str
    payload: Union[_ImagePayLoad, _TextPayLoad]
    sender: _Sender

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_MessagePayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        sender = _Sender.from_dict(payload_dict["sender"])
        if payload_dict["type"] == "image":
            payload = _ImagePayLoad.from_dict(payload_dict["payload"])
        elif payload_dict["type"] == "text":
            payload = _TextPayLoad.from_dict(payload_dict["payload"])
        else:
            raise NotImplementedError(
                f"Payload type {payload_dict['payload']['type']} not supported."
            )
        return cls(
            id=payload_dict["id"],
            source=payload_dict["source"],
            payload=payload,
            sender=sender,
        )


class _MessageEventPayLoad(SMBaseClass):
    """ """

    id: str
    _type: str
    destination: str
    payload: dict

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_MessageEventPayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            id=payload_dict["id"],
            _type=payload_dict["type"],
            destination=payload_dict["destination"],
            payload=payload_dict["payload"],
        )


class _BillingEventPayload(SMBaseClass):
    """

    Class for handling billing event payloads.

    Example:
    {'app': 'SyncMaster', 'timestamp': 1733229369353, 'version': 2, 'type': 'billing-event',
    'payload': {'deductions': {'type': 'service', 'model': 'CBP', 'source': 'whatsapp', 'billable': False},
    'references': {'id': '38034703-f873-40ba-b562-61849b1d6431', 'gsId': '1637d49e-f9c4-4361-8121-e4bdc108ebaf', 'conversationId': '42a9b4d675a89a483c676a6fd0a725e0', 'destination': '919582344421'}}}"""

    deductions: dict
    references: dict

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_BillingEventPayload":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            deductions=payload_dict["deductions"],
            references=payload_dict["references"],
        )


class _UserEventPayload(SMBaseClass):
    """ """

    phone: str
    _type: str

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_UserEventPayload":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        return cls(
            phone=payload_dict["phone"],
            _type=payload_dict["type"],
        )


class _PayLoad(SMBaseClass):
    """
    _PayLoad class represents a payload structure for the gupshup app.
    """

    payload: Union[
        _MessagePayLoad, _MessageEventPayLoad, _BillingEventPayload, _UserEventPayload
    ]

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "_PayLoad":
        """
        Creates a _PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            _PayLoad: The _PayLoad object created from the dictionary.
        """
        if payload_dict["type"] == "message":
            payload = _MessagePayLoad.from_dict(payload_dict["payload"])
        elif payload_dict["type"] == "message-event":
            payload = _MessageEventPayLoad.from_dict(payload_dict["payload"])
        elif payload_dict["type"] == "user-event":
            payload = _UserEventPayload.from_dict(payload_dict["payload"])
        else:
            raise NotImplementedError(
                f"Payload type {payload_dict['type']} not supported."
            )
        return cls(payload=payload)


class IncomingPayLoad(SMBaseClass):
    """
    IncomingPayLoad class for handling payload data.
    Attributes:
        app (str): The application name.
        timestamp (str): The timestamp of the payload.
        payload (_PayLoad): The payload data.
        is_dummy (bool): Indicates if the payload is a dummy. Defaults to False.
        _is_processed (bool): Indicates if the payload has been processed. Defaults to False.
    Methods:
        from_dict(cls, payload_dict: dict) -> "IncomingPayLoad":
        is_processed() -> bool:
            Returns the processed status of the payload.
        process(func: Callable, **kwargs) -> None:
    """

    app: str
    timestamp: int
    is_dummy: bool = False
    _is_processed: bool = False
    payload: _PayLoad = Field(..., description="The payload data.")

    @classmethod
    def from_dict(cls, payload_dict: dict) -> "IncomingPayLoad":
        """
        Creates a PayLoad object from a dictionary.
        Args:
            payload_dict (dict): The dictionary containing the payload data.
        Returns:
            PayLoad: The PayLoad object created from the dictionary.
        """
        payload:_PayLoad = _PayLoad.from_dict(payload_dict)
        app = payload_dict["app"]
        timestamp = payload_dict["timestamp"]
        is_dummy = payload_dict.get("is_dummy", False)
        return cls(app=app, timestamp=timestamp, payload=payload, is_dummy=is_dummy)

    @property
    def is_processed(self) -> bool:
        """Returns the processed status of the payload."""
        return self._is_processed

    def __call__(self, *args, **kwargs) -> dict:
        """
        Processes the incoming payload and updates the kwargs dictionary.

        If the instance is marked as a dummy, it sets the `_is_processed` attribute to True.
        If the payload is of type `_MessagePayLoad`, it converts the payload to a dictionary
        and updates the kwargs with the incoming payload and sender's phone number.
        Otherwise, it sets the `_is_processed` attribute to True and logs the payload type.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments to be updated with incoming payload data.

        Returns:
            dict: The updated kwargs dictionary.
        """
        if self.is_dummy:
            self._is_processed = True
        elif self.payload.payload.__class__.__name__ == "_MessagePayLoad":
            kwargs["incoming_payload"] = self.to_dict()
            kwargs["phone"] = self.payload.payload.sender.phone
            # print(kwargs)
            # run_as(jot_task, **kwargs)
        else:
            self._is_processed = True
            print(
                "Not a message payload, payload of type ",
                self.payload.payload.__class__.__name__,
            )
        return kwargs

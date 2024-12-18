# coding: utf-8

"""
    Bandwidth

    Bandwidth's Communication APIs

    The version of the OpenAPI document: 1.0.0
    Contact: letstalk@bandwidth.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from bandwidth.models.callback_method_enum import CallbackMethodEnum
from bandwidth.models.conference_member import ConferenceMember
from typing import Optional, Set
from typing_extensions import Self

class Conference(BaseModel):
    """
    Conference
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The Bandwidth-generated conference ID.")
    name: Optional[StrictStr] = Field(default=None, description="The name of the conference, as specified by your application.")
    created_time: Optional[datetime] = Field(default=None, description="The time the conference was initiated, in ISO 8601 format.", alias="createdTime")
    completed_time: Optional[datetime] = Field(default=None, description="The time the conference was terminated, in ISO 8601 format.", alias="completedTime")
    conference_event_url: Optional[StrictStr] = Field(default=None, description="The URL to send the conference-related events.", alias="conferenceEventUrl")
    conference_event_method: Optional[CallbackMethodEnum] = Field(default=CallbackMethodEnum.POST, alias="conferenceEventMethod")
    tag: Optional[StrictStr] = Field(default=None, description="The custom string attached to the conference that will be sent with callbacks.")
    active_members: Optional[List[ConferenceMember]] = Field(default=None, description="A list of active members of the conference. Omitted if this is a response to the [Get Conferences endpoint](/apis/voice#tag/Conferences/operation/listConferences).", alias="activeMembers")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["id", "name", "createdTime", "completedTime", "conferenceEventUrl", "conferenceEventMethod", "tag", "activeMembers"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Conference from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * Fields in `self.additional_properties` are added to the output dict.
        """
        excluded_fields: Set[str] = set([
            "additional_properties",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in active_members (list)
        _items = []
        if self.active_members:
            for _item in self.active_members:
                if _item:
                    _items.append(_item.to_dict())
            _dict['activeMembers'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if completed_time (nullable) is None
        # and model_fields_set contains the field
        if self.completed_time is None and "completed_time" in self.model_fields_set:
            _dict['completedTime'] = None

        # set to None if conference_event_url (nullable) is None
        # and model_fields_set contains the field
        if self.conference_event_url is None and "conference_event_url" in self.model_fields_set:
            _dict['conferenceEventUrl'] = None

        # set to None if conference_event_method (nullable) is None
        # and model_fields_set contains the field
        if self.conference_event_method is None and "conference_event_method" in self.model_fields_set:
            _dict['conferenceEventMethod'] = None

        # set to None if tag (nullable) is None
        # and model_fields_set contains the field
        if self.tag is None and "tag" in self.model_fields_set:
            _dict['tag'] = None

        # set to None if active_members (nullable) is None
        # and model_fields_set contains the field
        if self.active_members is None and "active_members" in self.model_fields_set:
            _dict['activeMembers'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Conference from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "createdTime": obj.get("createdTime"),
            "completedTime": obj.get("completedTime"),
            "conferenceEventUrl": obj.get("conferenceEventUrl"),
            "conferenceEventMethod": obj.get("conferenceEventMethod") if obj.get("conferenceEventMethod") is not None else CallbackMethodEnum.POST,
            "tag": obj.get("tag"),
            "activeMembers": [ConferenceMember.from_dict(_item) for _item in obj["activeMembers"]] if obj.get("activeMembers") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj



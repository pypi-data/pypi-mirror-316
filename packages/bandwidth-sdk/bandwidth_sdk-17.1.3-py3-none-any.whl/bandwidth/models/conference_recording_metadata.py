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
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from bandwidth.models.file_format_enum import FileFormatEnum
from typing import Optional, Set
from typing_extensions import Self

class ConferenceRecordingMetadata(BaseModel):
    """
    ConferenceRecordingMetadata
    """ # noqa: E501
    account_id: Optional[StrictStr] = Field(default=None, description="The user account associated with the call.", alias="accountId")
    conference_id: Optional[StrictStr] = Field(default=None, description="The unique, Bandwidth-generated ID of the conference that was recorded", alias="conferenceId")
    name: Optional[StrictStr] = Field(default=None, description="The user-specified name of the conference that was recorded")
    recording_id: Optional[StrictStr] = Field(default=None, description="The unique ID of this recording", alias="recordingId")
    duration: Optional[StrictStr] = Field(default=None, description="The duration of the recording in ISO-8601 format")
    channels: Optional[StrictInt] = Field(default=None, description="Always `1` for conference recordings; multi-channel recordings are not supported on conferences.")
    start_time: Optional[datetime] = Field(default=None, description="Time the call was started, in ISO 8601 format.", alias="startTime")
    end_time: Optional[datetime] = Field(default=None, description="The time that the recording ended in ISO-8601 format", alias="endTime")
    file_format: Optional[FileFormatEnum] = Field(default=None, alias="fileFormat")
    status: Optional[StrictStr] = Field(default=None, description="The current status of the process. For recording, current possible values are 'processing', 'partial', 'complete', 'deleted', and 'error'. For transcriptions, current possible values are 'none', 'processing', 'available', 'error', 'timeout', 'file-size-too-big', and 'file-size-too-small'. Additional states may be added in the future, so your application must be tolerant of unknown values.")
    media_url: Optional[StrictStr] = Field(default=None, description="The URL that can be used to download the recording. Only present if the recording is finished and may be downloaded.", alias="mediaUrl")
    recording_name: Optional[StrictStr] = Field(default=None, description="A name to identify this recording.", alias="recordingName")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["accountId", "conferenceId", "name", "recordingId", "duration", "channels", "startTime", "endTime", "fileFormat", "status", "mediaUrl", "recordingName"]

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
        """Create an instance of ConferenceRecordingMetadata from a JSON string"""
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
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if media_url (nullable) is None
        # and model_fields_set contains the field
        if self.media_url is None and "media_url" in self.model_fields_set:
            _dict['mediaUrl'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConferenceRecordingMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "accountId": obj.get("accountId"),
            "conferenceId": obj.get("conferenceId"),
            "name": obj.get("name"),
            "recordingId": obj.get("recordingId"),
            "duration": obj.get("duration"),
            "channels": obj.get("channels"),
            "startTime": obj.get("startTime"),
            "endTime": obj.get("endTime"),
            "fileFormat": obj.get("fileFormat"),
            "status": obj.get("status"),
            "mediaUrl": obj.get("mediaUrl"),
            "recordingName": obj.get("recordingName")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj



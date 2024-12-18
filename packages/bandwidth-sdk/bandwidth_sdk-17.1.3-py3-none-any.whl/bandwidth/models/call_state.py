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
from bandwidth.models.call_direction_enum import CallDirectionEnum
from typing import Optional, Set
from typing_extensions import Self

class CallState(BaseModel):
    """
    CallState
    """ # noqa: E501
    application_id: Optional[StrictStr] = Field(default=None, description="The application id associated with the call.", alias="applicationId")
    account_id: Optional[StrictStr] = Field(default=None, description="The account id associated with the call.", alias="accountId")
    call_id: Optional[StrictStr] = Field(default=None, description="The programmable voice API call ID.", alias="callId")
    parent_call_id: Optional[StrictStr] = Field(default=None, description="The A-leg call id, set only if this call is the B-leg of a [`<Transfer>`](/docs/voice/bxml/transfer).", alias="parentCallId")
    to: Optional[StrictStr] = Field(default=None, description="The phone number that received the call, in E.164 format (e.g. +15555555555), or if the call was to a SIP URI, the SIP URI.")
    var_from: Optional[StrictStr] = Field(default=None, description="The phone number that made the call, in E.164 format (e.g. +15555555555).", alias="from")
    direction: Optional[CallDirectionEnum] = None
    state: Optional[StrictStr] = Field(default=None, description="The current state of the call. Current possible values are `queued`, `initiated`, `answered` and `disconnected`. Additional states may be added in the future, so your application must be tolerant of unknown values.")
    stir_shaken: Optional[Dict[str, StrictStr]] = Field(default=None, description="For inbound calls, the Bandwidth STIR/SHAKEN implementation will verify the information provided in the inbound invite request `Identity` header. The verification status is stored in the call state `stirShaken` property as follows.  | Property          | Description | |:------------------|:------------| | verstat | (optional) The verification status indicating whether the verification was successful or not. Possible values are `TN-Verification-Passed` or `TN-Verification-Failed`. | | attestationIndicator | (optional) The attestation level verified by Bandwidth. Possible values are `A` (full), `B` (partial) or `C` (gateway). | | originatingId | (optional) A unique origination identifier. |  Note that these are common properties but that the `stirShaken` object is free form and can contain other key-value pairs.  More information: [Understanding STIR/SHAKEN](https://www.bandwidth.com/regulations/stir-shaken).", alias="stirShaken")
    identity: Optional[StrictStr] = Field(default=None, description="The value of the `Identity` header from the inbound invite request. Only present for inbound calls and if the account is configured to forward this header.")
    enqueued_time: Optional[datetime] = Field(default=None, description="The time this call was placed in queue.", alias="enqueuedTime")
    start_time: Optional[datetime] = Field(default=None, description="The time the call was initiated, in ISO 8601 format. `null` if the call is still in your queue.", alias="startTime")
    answer_time: Optional[datetime] = Field(default=None, description="Populated once the call has been answered, with the time in ISO 8601 format.", alias="answerTime")
    end_time: Optional[datetime] = Field(default=None, description="Populated once the call has ended, with the time in ISO 8601 format.", alias="endTime")
    disconnect_cause: Optional[StrictStr] = Field(default=None, description="| Cause | Description | |:------|:------------| | `hangup`| One party hung up the call, a [`<Hangup>`](../../bxml/verbs/hangup.md) verb was executed, or there was no more BXML to execute; it indicates that the call ended normally. | | `busy` | Callee was busy. | | `timeout` | Call wasn't answered before the `callTimeout` was reached. | | `cancel` | Call was cancelled by its originator while it was ringing. | | `rejected` | Call was rejected by the callee. | | `callback-error` | BXML callback couldn't be delivered to your callback server. | | `invalid-bxml` | Invalid BXML was returned in response to a callback. | | `application-error` | An unsupported action was tried on the call, e.g. trying to play a .ogg audio. | | `account-limit` | Account rate limits were reached. | | `node-capacity-exceeded` | System maximum capacity was reached. | | `error` | Some error not described in any of the other causes happened on the call. | | `unknown` | Unknown error happened on the call. |  Note: This list is not exhaustive and other values can appear in the future.", alias="disconnectCause")
    error_message: Optional[StrictStr] = Field(default=None, description="Populated only if the call ended with an error, with text explaining the reason.", alias="errorMessage")
    error_id: Optional[StrictStr] = Field(default=None, description="Populated only if the call ended with an error, with a Bandwidth internal id that references the error event.", alias="errorId")
    last_update: Optional[datetime] = Field(default=None, description="The last time the call had a state update, in ISO 8601 format.", alias="lastUpdate")
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = ["applicationId", "accountId", "callId", "parentCallId", "to", "from", "direction", "state", "stirShaken", "identity", "enqueuedTime", "startTime", "answerTime", "endTime", "disconnectCause", "errorMessage", "errorId", "lastUpdate"]

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
        """Create an instance of CallState from a JSON string"""
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

        # set to None if parent_call_id (nullable) is None
        # and model_fields_set contains the field
        if self.parent_call_id is None and "parent_call_id" in self.model_fields_set:
            _dict['parentCallId'] = None

        # set to None if stir_shaken (nullable) is None
        # and model_fields_set contains the field
        if self.stir_shaken is None and "stir_shaken" in self.model_fields_set:
            _dict['stirShaken'] = None

        # set to None if identity (nullable) is None
        # and model_fields_set contains the field
        if self.identity is None and "identity" in self.model_fields_set:
            _dict['identity'] = None

        # set to None if enqueued_time (nullable) is None
        # and model_fields_set contains the field
        if self.enqueued_time is None and "enqueued_time" in self.model_fields_set:
            _dict['enqueuedTime'] = None

        # set to None if start_time (nullable) is None
        # and model_fields_set contains the field
        if self.start_time is None and "start_time" in self.model_fields_set:
            _dict['startTime'] = None

        # set to None if answer_time (nullable) is None
        # and model_fields_set contains the field
        if self.answer_time is None and "answer_time" in self.model_fields_set:
            _dict['answerTime'] = None

        # set to None if end_time (nullable) is None
        # and model_fields_set contains the field
        if self.end_time is None and "end_time" in self.model_fields_set:
            _dict['endTime'] = None

        # set to None if disconnect_cause (nullable) is None
        # and model_fields_set contains the field
        if self.disconnect_cause is None and "disconnect_cause" in self.model_fields_set:
            _dict['disconnectCause'] = None

        # set to None if error_message (nullable) is None
        # and model_fields_set contains the field
        if self.error_message is None and "error_message" in self.model_fields_set:
            _dict['errorMessage'] = None

        # set to None if error_id (nullable) is None
        # and model_fields_set contains the field
        if self.error_id is None and "error_id" in self.model_fields_set:
            _dict['errorId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CallState from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "applicationId": obj.get("applicationId"),
            "accountId": obj.get("accountId"),
            "callId": obj.get("callId"),
            "parentCallId": obj.get("parentCallId"),
            "to": obj.get("to"),
            "from": obj.get("from"),
            "direction": obj.get("direction"),
            "state": obj.get("state"),
            "stirShaken": obj.get("stirShaken"),
            "identity": obj.get("identity"),
            "enqueuedTime": obj.get("enqueuedTime"),
            "startTime": obj.get("startTime"),
            "answerTime": obj.get("answerTime"),
            "endTime": obj.get("endTime"),
            "disconnectCause": obj.get("disconnectCause"),
            "errorMessage": obj.get("errorMessage"),
            "errorId": obj.get("errorId"),
            "lastUpdate": obj.get("lastUpdate")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj



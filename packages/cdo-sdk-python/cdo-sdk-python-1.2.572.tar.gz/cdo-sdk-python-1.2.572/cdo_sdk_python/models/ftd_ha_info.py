# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.ha_node import HaNode
from typing import Optional, Set
from typing_extensions import Self

class FtdHaInfo(BaseModel):
    """
    (High Availability Devices managed by FMC only) High-Available information information. Note: Security Cloud Control represents all of the nodes on an FTD cluster in a single device record with the UID of the cluster control node.
    """ # noqa: E501
    ha_pair_uid: Optional[StrictStr] = Field(default=None, description="The unique identifier, represented as a UUID, of the HA Pair, on the FMC", alias="haPairUid")
    primary_node: Optional[HaNode] = Field(default=None, alias="primaryNode")
    secondary_node: Optional[HaNode] = Field(default=None, alias="secondaryNode")
    ha_node_type: Optional[StrictStr] = Field(default=None, description="(on-prem FMC-managed FTDs only) Information on the type of this node in the HA Pair. Note: Each node in an on-prem-FMC-managed FTD HA Pair is represented as a separate device entry in the API.", alias="haNodeType")
    current_role: Optional[StrictStr] = Field(default=None, description="(on-prem FMC-managed FTDs only) Information on the current role of the node in the HA Pair. Note: Each node in an on-prem-FMC-managed FTD HA Pair is represented as a separate device entry in the API.", alias="currentRole")
    __properties: ClassVar[List[str]] = ["haPairUid", "primaryNode", "secondaryNode", "haNodeType", "currentRole"]

    @field_validator('ha_node_type')
    def ha_node_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PRIMARY', 'SECONDARY']):
            raise ValueError("must be one of enum values ('PRIMARY', 'SECONDARY')")
        return value

    @field_validator('current_role')
    def current_role_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ACTIVE', 'STANDBY']):
            raise ValueError("must be one of enum values ('ACTIVE', 'STANDBY')")
        return value

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
        """Create an instance of FtdHaInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of primary_node
        if self.primary_node:
            _dict['primaryNode'] = self.primary_node.to_dict()
        # override the default output from pydantic by calling `to_dict()` of secondary_node
        if self.secondary_node:
            _dict['secondaryNode'] = self.secondary_node.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FtdHaInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "haPairUid": obj.get("haPairUid"),
            "primaryNode": HaNode.from_dict(obj["primaryNode"]) if obj.get("primaryNode") is not None else None,
            "secondaryNode": HaNode.from_dict(obj["secondaryNode"]) if obj.get("secondaryNode") is not None else None,
            "haNodeType": obj.get("haNodeType"),
            "currentRole": obj.get("currentRole")
        })
        return _obj



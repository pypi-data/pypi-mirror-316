from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NewBotRequest")


@_attrs_define
class NewBotRequest:
    """
    Example:
        {'api_key': '123e4567-e89b-12d3-a456-426614174000', 'api_secret': 'qwerty123456', 'bot_token':
            '7516569554:AAFj-G7jpoBuj2UK5wBB7xEQxBuRVAPQCrU', 'integration_uuid': '123e4567-e89b-12d3-a456-426614174000'}

    Attributes:
        integration_uuid (UUID): Integration UUID related to that bot
        bot_token (str): Bot token from Telegram API
        api_key (UUID): API key for our backend api
        api_secret (str): API secret for our backend api. We are also using it as telegram webhook secret
    """

    integration_uuid: UUID
    bot_token: str
    api_key: UUID
    api_secret: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        integration_uuid = str(self.integration_uuid)

        bot_token = self.bot_token

        api_key = str(self.api_key)

        api_secret = self.api_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "integration_uuid": integration_uuid,
                "bot_token": bot_token,
                "api_key": api_key,
                "api_secret": api_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        integration_uuid = UUID(d.pop("integration_uuid"))

        bot_token = d.pop("bot_token")

        api_key = UUID(d.pop("api_key"))

        api_secret = d.pop("api_secret")

        new_bot_request = cls(
            integration_uuid=integration_uuid,
            bot_token=bot_token,
            api_key=api_key,
            api_secret=api_secret,
        )

        new_bot_request.additional_properties = d
        return new_bot_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

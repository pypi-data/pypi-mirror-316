"""
Type annotations for notifications service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_notifications.client import UserNotificationsClient

    session = get_session()
    async with session.create_client("notifications") as client:
        client: UserNotificationsClient
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListChannelsPaginator,
    ListEventRulesPaginator,
    ListNotificationConfigurationsPaginator,
    ListNotificationEventsPaginator,
    ListNotificationHubsPaginator,
)
from .type_defs import (
    AssociateChannelRequestRequestTypeDef,
    CreateEventRuleRequestRequestTypeDef,
    CreateEventRuleResponseTypeDef,
    CreateNotificationConfigurationRequestRequestTypeDef,
    CreateNotificationConfigurationResponseTypeDef,
    DeleteEventRuleRequestRequestTypeDef,
    DeleteNotificationConfigurationRequestRequestTypeDef,
    DeregisterNotificationHubRequestRequestTypeDef,
    DeregisterNotificationHubResponseTypeDef,
    DisassociateChannelRequestRequestTypeDef,
    GetEventRuleRequestRequestTypeDef,
    GetEventRuleResponseTypeDef,
    GetNotificationConfigurationRequestRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetNotificationEventRequestRequestTypeDef,
    GetNotificationEventResponseTypeDef,
    ListChannelsRequestRequestTypeDef,
    ListChannelsResponseTypeDef,
    ListEventRulesRequestRequestTypeDef,
    ListEventRulesResponseTypeDef,
    ListNotificationConfigurationsRequestRequestTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListNotificationEventsRequestRequestTypeDef,
    ListNotificationEventsResponseTypeDef,
    ListNotificationHubsRequestRequestTypeDef,
    ListNotificationHubsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterNotificationHubRequestRequestTypeDef,
    RegisterNotificationHubResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateEventRuleRequestRequestTypeDef,
    UpdateEventRuleResponseTypeDef,
    UpdateNotificationConfigurationRequestRequestTypeDef,
    UpdateNotificationConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("UserNotificationsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class UserNotificationsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        UserNotificationsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#generate_presigned_url)
        """

    async def close(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/close.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#close)
        """

    async def associate_channel(
        self, **kwargs: Unpack[AssociateChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a delivery <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/managing-delivery-channels.html">Channel</a>
        with a particular NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/associate_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#associate_channel)
        """

    async def create_event_rule(
        self, **kwargs: Unpack[CreateEventRuleRequestRequestTypeDef]
    ) -> CreateEventRuleResponseTypeDef:
        """
        Creates an <a
        href="https://docs.aws.amazon.com/notifications/latest/userguide/glossary.html">EventRule</a>
        that is associated with a specified Notification Configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_event_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#create_event_rule)
        """

    async def create_notification_configuration(
        self, **kwargs: Unpack[CreateNotificationConfigurationRequestRequestTypeDef]
    ) -> CreateNotificationConfigurationResponseTypeDef:
        """
        Creates a new NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/create_notification_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#create_notification_configuration)
        """

    async def delete_event_rule(
        self, **kwargs: Unpack[DeleteEventRuleRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_event_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#delete_event_rule)
        """

    async def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/delete_notification_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#delete_notification_configuration)
        """

    async def deregister_notification_hub(
        self, **kwargs: Unpack[DeregisterNotificationHubRequestRequestTypeDef]
    ) -> DeregisterNotificationHubResponseTypeDef:
        """
        Deregisters a NotificationHub in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/deregister_notification_hub.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#deregister_notification_hub)
        """

    async def disassociate_channel(
        self, **kwargs: Unpack[DisassociateChannelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a Channel from a specified NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/disassociate_channel.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#disassociate_channel)
        """

    async def get_event_rule(
        self, **kwargs: Unpack[GetEventRuleRequestRequestTypeDef]
    ) -> GetEventRuleResponseTypeDef:
        """
        Returns a specified EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_event_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_event_rule)
        """

    async def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Returns a specified NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_notification_configuration)
        """

    async def get_notification_event(
        self, **kwargs: Unpack[GetNotificationEventRequestRequestTypeDef]
    ) -> GetNotificationEventResponseTypeDef:
        """
        Returns a specified NotificationEvent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_notification_event.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_notification_event)
        """

    async def list_channels(
        self, **kwargs: Unpack[ListChannelsRequestRequestTypeDef]
    ) -> ListChannelsResponseTypeDef:
        """
        Returns a list of Channels for a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_channels.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_channels)
        """

    async def list_event_rules(
        self, **kwargs: Unpack[ListEventRulesRequestRequestTypeDef]
    ) -> ListEventRulesResponseTypeDef:
        """
        Returns a list of EventRules according to specified filters, in reverse
        chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_event_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_event_rules)
        """

    async def list_notification_configurations(
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestRequestTypeDef]
    ) -> ListNotificationConfigurationsResponseTypeDef:
        """
        Returns a list of abbreviated NotificationConfigurations according to specified
        filters, in reverse chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_configurations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_configurations)
        """

    async def list_notification_events(
        self, **kwargs: Unpack[ListNotificationEventsRequestRequestTypeDef]
    ) -> ListNotificationEventsResponseTypeDef:
        """
        Returns a list of NotificationEvents according to specified filters, in reverse
        chronological order (newest first).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_events)
        """

    async def list_notification_hubs(
        self, **kwargs: Unpack[ListNotificationHubsRequestRequestTypeDef]
    ) -> ListNotificationHubsResponseTypeDef:
        """
        Returns a list of NotificationHubs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_notification_hubs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_notification_hubs)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#list_tags_for_resource)
        """

    async def register_notification_hub(
        self, **kwargs: Unpack[RegisterNotificationHubRequestRequestTypeDef]
    ) -> RegisterNotificationHubResponseTypeDef:
        """
        Registers a NotificationHub in the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/register_notification_hub.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#register_notification_hub)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Tags the resource with a tag key and value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Untags a resource with a specified Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#untag_resource)
        """

    async def update_event_rule(
        self, **kwargs: Unpack[UpdateEventRuleRequestRequestTypeDef]
    ) -> UpdateEventRuleResponseTypeDef:
        """
        Updates an existing EventRule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_event_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#update_event_rule)
        """

    async def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationRequestRequestTypeDef]
    ) -> UpdateNotificationConfigurationResponseTypeDef:
        """
        Updates a NotificationConfiguration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/update_notification_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#update_notification_configuration)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_event_rules"]) -> ListEventRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_configurations"]
    ) -> ListNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_events"]
    ) -> ListNotificationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_notification_hubs"]
    ) -> ListNotificationHubsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/#get_paginator)
        """

    async def __aenter__(self) -> "UserNotificationsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notifications.html#UserNotifications.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notifications/client/)
        """

"""
Type annotations for notificationscontacts service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_notificationscontacts.client import UserNotificationsContactsClient
    from types_aiobotocore_notificationscontacts.paginator import (
        ListEmailContactsPaginator,
    )

    session = get_session()
    with session.create_client("notificationscontacts") as client:
        client: UserNotificationsContactsClient

        list_email_contacts_paginator: ListEmailContactsPaginator = client.get_paginator("list_email_contacts")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEmailContactsRequestListEmailContactsPaginateTypeDef,
    ListEmailContactsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListEmailContactsPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListEmailContactsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/#listemailcontactspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListEmailContactsRequestListEmailContactsPaginateTypeDef]
    ) -> AsyncIterator[ListEmailContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/notificationscontacts/paginator/ListEmailContacts.html#UserNotificationsContacts.Paginator.ListEmailContacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_notificationscontacts/paginators/#listemailcontactspaginator)
        """

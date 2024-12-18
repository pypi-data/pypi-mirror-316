"""
Type annotations for taxsettings service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_taxsettings.client import TaxSettingsClient
    from types_aiobotocore_taxsettings.paginator import (
        ListSupplementalTaxRegistrationsPaginator,
        ListTaxExemptionsPaginator,
        ListTaxRegistrationsPaginator,
    )

    session = get_session()
    with session.create_client("taxsettings") as client:
        client: TaxSettingsClient

        list_supplemental_tax_registrations_paginator: ListSupplementalTaxRegistrationsPaginator = client.get_paginator("list_supplemental_tax_registrations")
        list_tax_exemptions_paginator: ListTaxExemptionsPaginator = client.get_paginator("list_tax_exemptions")
        list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListSupplementalTaxRegistrationsRequestListSupplementalTaxRegistrationsPaginateTypeDef,
    ListSupplementalTaxRegistrationsResponseTypeDef,
    ListTaxExemptionsRequestListTaxExemptionsPaginateTypeDef,
    ListTaxExemptionsResponseTypeDef,
    ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef,
    ListTaxRegistrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSupplementalTaxRegistrationsPaginator",
    "ListTaxExemptionsPaginator",
    "ListTaxRegistrationsPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListSupplementalTaxRegistrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListSupplementalTaxRegistrations.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListSupplementalTaxRegistrationsRequestListSupplementalTaxRegistrationsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListSupplementalTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListSupplementalTaxRegistrations.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
        """

class ListTaxExemptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxExemptions.html#TaxSettings.Paginator.ListTaxExemptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxexemptionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTaxExemptionsRequestListTaxExemptionsPaginateTypeDef]
    ) -> AsyncIterator[ListTaxExemptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxExemptions.html#TaxSettings.Paginator.ListTaxExemptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxexemptionspaginator)
        """

class ListTaxRegistrationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListTaxRegistrationsRequestListTaxRegistrationsPaginateTypeDef]
    ) -> AsyncIterator[ListTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
        """

"""
Type annotations for apigateway service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_apigateway.client import APIGatewayClient
    from mypy_boto3_apigateway.paginator import (
        GetApiKeysPaginator,
        GetAuthorizersPaginator,
        GetBasePathMappingsPaginator,
        GetClientCertificatesPaginator,
        GetDeploymentsPaginator,
        GetDocumentationPartsPaginator,
        GetDocumentationVersionsPaginator,
        GetDomainNamesPaginator,
        GetGatewayResponsesPaginator,
        GetModelsPaginator,
        GetRequestValidatorsPaginator,
        GetResourcesPaginator,
        GetRestApisPaginator,
        GetSdkTypesPaginator,
        GetUsagePaginator,
        GetUsagePlanKeysPaginator,
        GetUsagePlansPaginator,
        GetVpcLinksPaginator,
    )

    session = Session()
    client: APIGatewayClient = session.client("apigateway")

    get_api_keys_paginator: GetApiKeysPaginator = client.get_paginator("get_api_keys")
    get_authorizers_paginator: GetAuthorizersPaginator = client.get_paginator("get_authorizers")
    get_base_path_mappings_paginator: GetBasePathMappingsPaginator = client.get_paginator("get_base_path_mappings")
    get_client_certificates_paginator: GetClientCertificatesPaginator = client.get_paginator("get_client_certificates")
    get_deployments_paginator: GetDeploymentsPaginator = client.get_paginator("get_deployments")
    get_documentation_parts_paginator: GetDocumentationPartsPaginator = client.get_paginator("get_documentation_parts")
    get_documentation_versions_paginator: GetDocumentationVersionsPaginator = client.get_paginator("get_documentation_versions")
    get_domain_names_paginator: GetDomainNamesPaginator = client.get_paginator("get_domain_names")
    get_gateway_responses_paginator: GetGatewayResponsesPaginator = client.get_paginator("get_gateway_responses")
    get_models_paginator: GetModelsPaginator = client.get_paginator("get_models")
    get_request_validators_paginator: GetRequestValidatorsPaginator = client.get_paginator("get_request_validators")
    get_resources_paginator: GetResourcesPaginator = client.get_paginator("get_resources")
    get_rest_apis_paginator: GetRestApisPaginator = client.get_paginator("get_rest_apis")
    get_sdk_types_paginator: GetSdkTypesPaginator = client.get_paginator("get_sdk_types")
    get_usage_paginator: GetUsagePaginator = client.get_paginator("get_usage")
    get_usage_plan_keys_paginator: GetUsagePlanKeysPaginator = client.get_paginator("get_usage_plan_keys")
    get_usage_plans_paginator: GetUsagePlansPaginator = client.get_paginator("get_usage_plans")
    get_vpc_links_paginator: GetVpcLinksPaginator = client.get_paginator("get_vpc_links")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ApiKeysTypeDef,
    AuthorizersTypeDef,
    BasePathMappingsTypeDef,
    ClientCertificatesTypeDef,
    DeploymentsTypeDef,
    DocumentationPartsTypeDef,
    DocumentationVersionsTypeDef,
    DomainNamesTypeDef,
    GatewayResponsesTypeDef,
    GetApiKeysRequestGetApiKeysPaginateTypeDef,
    GetAuthorizersRequestGetAuthorizersPaginateTypeDef,
    GetBasePathMappingsRequestGetBasePathMappingsPaginateTypeDef,
    GetClientCertificatesRequestGetClientCertificatesPaginateTypeDef,
    GetDeploymentsRequestGetDeploymentsPaginateTypeDef,
    GetDocumentationPartsRequestGetDocumentationPartsPaginateTypeDef,
    GetDocumentationVersionsRequestGetDocumentationVersionsPaginateTypeDef,
    GetDomainNamesRequestGetDomainNamesPaginateTypeDef,
    GetGatewayResponsesRequestGetGatewayResponsesPaginateTypeDef,
    GetModelsRequestGetModelsPaginateTypeDef,
    GetRequestValidatorsRequestGetRequestValidatorsPaginateTypeDef,
    GetResourcesRequestGetResourcesPaginateTypeDef,
    GetRestApisRequestGetRestApisPaginateTypeDef,
    GetSdkTypesRequestGetSdkTypesPaginateTypeDef,
    GetUsagePlanKeysRequestGetUsagePlanKeysPaginateTypeDef,
    GetUsagePlansRequestGetUsagePlansPaginateTypeDef,
    GetUsageRequestGetUsagePaginateTypeDef,
    GetVpcLinksRequestGetVpcLinksPaginateTypeDef,
    ModelsTypeDef,
    RequestValidatorsTypeDef,
    ResourcesTypeDef,
    RestApisTypeDef,
    SdkTypesTypeDef,
    UsagePlanKeysTypeDef,
    UsagePlansTypeDef,
    UsageTypeDef,
    VpcLinksTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetApiKeysPaginator",
    "GetAuthorizersPaginator",
    "GetBasePathMappingsPaginator",
    "GetClientCertificatesPaginator",
    "GetDeploymentsPaginator",
    "GetDocumentationPartsPaginator",
    "GetDocumentationVersionsPaginator",
    "GetDomainNamesPaginator",
    "GetGatewayResponsesPaginator",
    "GetModelsPaginator",
    "GetRequestValidatorsPaginator",
    "GetResourcesPaginator",
    "GetRestApisPaginator",
    "GetSdkTypesPaginator",
    "GetUsagePaginator",
    "GetUsagePlanKeysPaginator",
    "GetUsagePlansPaginator",
    "GetVpcLinksPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetApiKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getapikeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetApiKeysRequestGetApiKeysPaginateTypeDef]
    ) -> _PageIterator[ApiKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetApiKeys.html#APIGateway.Paginator.GetApiKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getapikeyspaginator)
        """

class GetAuthorizersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getauthorizerspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetAuthorizersRequestGetAuthorizersPaginateTypeDef]
    ) -> _PageIterator[AuthorizersTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetAuthorizers.html#APIGateway.Paginator.GetAuthorizers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getauthorizerspaginator)
        """

class GetBasePathMappingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getbasepathmappingspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetBasePathMappingsRequestGetBasePathMappingsPaginateTypeDef]
    ) -> _PageIterator[BasePathMappingsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetBasePathMappings.html#APIGateway.Paginator.GetBasePathMappings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getbasepathmappingspaginator)
        """

class GetClientCertificatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getclientcertificatespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetClientCertificatesRequestGetClientCertificatesPaginateTypeDef]
    ) -> _PageIterator[ClientCertificatesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetClientCertificates.html#APIGateway.Paginator.GetClientCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getclientcertificatespaginator)
        """

class GetDeploymentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdeploymentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDeploymentsRequestGetDeploymentsPaginateTypeDef]
    ) -> _PageIterator[DeploymentsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDeployments.html#APIGateway.Paginator.GetDeployments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdeploymentspaginator)
        """

class GetDocumentationPartsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdocumentationpartspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDocumentationPartsRequestGetDocumentationPartsPaginateTypeDef]
    ) -> _PageIterator[DocumentationPartsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationParts.html#APIGateway.Paginator.GetDocumentationParts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdocumentationpartspaginator)
        """

class GetDocumentationVersionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdocumentationversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[GetDocumentationVersionsRequestGetDocumentationVersionsPaginateTypeDef],
    ) -> _PageIterator[DocumentationVersionsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDocumentationVersions.html#APIGateway.Paginator.GetDocumentationVersions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdocumentationversionspaginator)
        """

class GetDomainNamesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdomainnamespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetDomainNamesRequestGetDomainNamesPaginateTypeDef]
    ) -> _PageIterator[DomainNamesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetDomainNames.html#APIGateway.Paginator.GetDomainNames.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getdomainnamespaginator)
        """

class GetGatewayResponsesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getgatewayresponsespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetGatewayResponsesRequestGetGatewayResponsesPaginateTypeDef]
    ) -> _PageIterator[GatewayResponsesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetGatewayResponses.html#APIGateway.Paginator.GetGatewayResponses.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getgatewayresponsespaginator)
        """

class GetModelsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getmodelspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetModelsRequestGetModelsPaginateTypeDef]
    ) -> _PageIterator[ModelsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetModels.html#APIGateway.Paginator.GetModels.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getmodelspaginator)
        """

class GetRequestValidatorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getrequestvalidatorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRequestValidatorsRequestGetRequestValidatorsPaginateTypeDef]
    ) -> _PageIterator[RequestValidatorsTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRequestValidators.html#APIGateway.Paginator.GetRequestValidators.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getrequestvalidatorspaginator)
        """

class GetResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getresourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetResourcesRequestGetResourcesPaginateTypeDef]
    ) -> _PageIterator[ResourcesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetResources.html#APIGateway.Paginator.GetResources.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getresourcespaginator)
        """

class GetRestApisPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getrestapispaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetRestApisRequestGetRestApisPaginateTypeDef]
    ) -> _PageIterator[RestApisTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetRestApis.html#APIGateway.Paginator.GetRestApis.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getrestapispaginator)
        """

class GetSdkTypesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getsdktypespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetSdkTypesRequestGetSdkTypesPaginateTypeDef]
    ) -> _PageIterator[SdkTypesTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetSdkTypes.html#APIGateway.Paginator.GetSdkTypes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getsdktypespaginator)
        """

class GetUsagePaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusagepaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsageRequestGetUsagePaginateTypeDef]
    ) -> _PageIterator[UsageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsage.html#APIGateway.Paginator.GetUsage.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusagepaginator)
        """

class GetUsagePlanKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusageplankeyspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsagePlanKeysRequestGetUsagePlanKeysPaginateTypeDef]
    ) -> _PageIterator[UsagePlanKeysTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlanKeys.html#APIGateway.Paginator.GetUsagePlanKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusageplankeyspaginator)
        """

class GetUsagePlansPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusageplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetUsagePlansRequestGetUsagePlansPaginateTypeDef]
    ) -> _PageIterator[UsagePlansTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetUsagePlans.html#APIGateway.Paginator.GetUsagePlans.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getusageplanspaginator)
        """

class GetVpcLinksPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getvpclinkspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[GetVpcLinksRequestGetVpcLinksPaginateTypeDef]
    ) -> _PageIterator[VpcLinksTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apigateway/paginator/GetVpcLinks.html#APIGateway.Paginator.GetVpcLinks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apigateway/paginators/#getvpclinkspaginator)
        """

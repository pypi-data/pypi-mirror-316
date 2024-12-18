"""
Type annotations for qbusiness service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_qbusiness.client import QBusinessClient
    from types_aiobotocore_qbusiness.paginator import (
        GetChatControlsConfigurationPaginator,
        ListApplicationsPaginator,
        ListAttachmentsPaginator,
        ListConversationsPaginator,
        ListDataAccessorsPaginator,
        ListDataSourceSyncJobsPaginator,
        ListDataSourcesPaginator,
        ListDocumentsPaginator,
        ListGroupsPaginator,
        ListIndicesPaginator,
        ListMessagesPaginator,
        ListPluginActionsPaginator,
        ListPluginTypeActionsPaginator,
        ListPluginTypeMetadataPaginator,
        ListPluginsPaginator,
        ListRetrieversPaginator,
        ListWebExperiencesPaginator,
        SearchRelevantContentPaginator,
    )

    session = get_session()
    with session.create_client("qbusiness") as client:
        client: QBusinessClient

        get_chat_controls_configuration_paginator: GetChatControlsConfigurationPaginator = client.get_paginator("get_chat_controls_configuration")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_attachments_paginator: ListAttachmentsPaginator = client.get_paginator("list_attachments")
        list_conversations_paginator: ListConversationsPaginator = client.get_paginator("list_conversations")
        list_data_accessors_paginator: ListDataAccessorsPaginator = client.get_paginator("list_data_accessors")
        list_data_source_sync_jobs_paginator: ListDataSourceSyncJobsPaginator = client.get_paginator("list_data_source_sync_jobs")
        list_data_sources_paginator: ListDataSourcesPaginator = client.get_paginator("list_data_sources")
        list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
        list_messages_paginator: ListMessagesPaginator = client.get_paginator("list_messages")
        list_plugin_actions_paginator: ListPluginActionsPaginator = client.get_paginator("list_plugin_actions")
        list_plugin_type_actions_paginator: ListPluginTypeActionsPaginator = client.get_paginator("list_plugin_type_actions")
        list_plugin_type_metadata_paginator: ListPluginTypeMetadataPaginator = client.get_paginator("list_plugin_type_metadata")
        list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
        list_retrievers_paginator: ListRetrieversPaginator = client.get_paginator("list_retrievers")
        list_web_experiences_paginator: ListWebExperiencesPaginator = client.get_paginator("list_web_experiences")
        search_relevant_content_paginator: SearchRelevantContentPaginator = client.get_paginator("search_relevant_content")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef,
    GetChatControlsConfigurationResponseTypeDef,
    ListApplicationsRequestListApplicationsPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListAttachmentsRequestListAttachmentsPaginateTypeDef,
    ListAttachmentsResponseTypeDef,
    ListConversationsRequestListConversationsPaginateTypeDef,
    ListConversationsResponseTypeDef,
    ListDataAccessorsRequestListDataAccessorsPaginateTypeDef,
    ListDataAccessorsResponseTypeDef,
    ListDataSourcesRequestListDataSourcesPaginateTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListDocumentsRequestListDocumentsPaginateTypeDef,
    ListDocumentsResponseTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResponseTypeDef,
    ListIndicesRequestListIndicesPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListMessagesRequestListMessagesPaginateTypeDef,
    ListMessagesResponseTypeDef,
    ListPluginActionsRequestListPluginActionsPaginateTypeDef,
    ListPluginActionsResponseTypeDef,
    ListPluginsRequestListPluginsPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef,
    ListPluginTypeActionsResponseTypeDef,
    ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef,
    ListPluginTypeMetadataResponseTypeDef,
    ListRetrieversRequestListRetrieversPaginateTypeDef,
    ListRetrieversResponseTypeDef,
    ListWebExperiencesRequestListWebExperiencesPaginateTypeDef,
    ListWebExperiencesResponseTypeDef,
    SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef,
    SearchRelevantContentResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetChatControlsConfigurationPaginator",
    "ListApplicationsPaginator",
    "ListAttachmentsPaginator",
    "ListConversationsPaginator",
    "ListDataAccessorsPaginator",
    "ListDataSourceSyncJobsPaginator",
    "ListDataSourcesPaginator",
    "ListDocumentsPaginator",
    "ListGroupsPaginator",
    "ListIndicesPaginator",
    "ListMessagesPaginator",
    "ListPluginActionsPaginator",
    "ListPluginTypeActionsPaginator",
    "ListPluginTypeMetadataPaginator",
    "ListPluginsPaginator",
    "ListRetrieversPaginator",
    "ListWebExperiencesPaginator",
    "SearchRelevantContentPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetChatControlsConfigurationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            GetChatControlsConfigurationRequestGetChatControlsConfigurationPaginateTypeDef
        ],
    ) -> AsyncIterator[GetChatControlsConfigurationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/GetChatControlsConfiguration.html#QBusiness.Paginator.GetChatControlsConfiguration.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#getchatcontrolsconfigurationpaginator)
        """

class ListApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listapplicationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListApplicationsRequestListApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListApplications.html#QBusiness.Paginator.ListApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listapplicationspaginator)
        """

class ListAttachmentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listattachmentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAttachmentsRequestListAttachmentsPaginateTypeDef]
    ) -> AsyncIterator[ListAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListAttachments.html#QBusiness.Paginator.ListAttachments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listattachmentspaginator)
        """

class ListConversationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listconversationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListConversationsRequestListConversationsPaginateTypeDef]
    ) -> AsyncIterator[ListConversationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListConversations.html#QBusiness.Paginator.ListConversations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listconversationspaginator)
        """

class ListDataAccessorsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdataaccessorspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataAccessorsRequestListDataAccessorsPaginateTypeDef]
    ) -> AsyncIterator[ListDataAccessorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataAccessors.html#QBusiness.Paginator.ListDataAccessors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdataaccessorspaginator)
        """

class ListDataSourceSyncJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcesyncjobspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestListDataSourceSyncJobsPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourceSyncJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSourceSyncJobs.html#QBusiness.Paginator.ListDataSourceSyncJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcesyncjobspaginator)
        """

class ListDataSourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDataSourcesRequestListDataSourcesPaginateTypeDef]
    ) -> AsyncIterator[ListDataSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDataSources.html#QBusiness.Paginator.ListDataSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdatasourcespaginator)
        """

class ListDocumentsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdocumentspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListDocumentsRequestListDocumentsPaginateTypeDef]
    ) -> AsyncIterator[ListDocumentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListDocuments.html#QBusiness.Paginator.ListDocuments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listdocumentspaginator)
        """

class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListGroups.html#QBusiness.Paginator.ListGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listgroupspaginator)
        """

class ListIndicesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listindicespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListIndicesRequestListIndicesPaginateTypeDef]
    ) -> AsyncIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListIndices.html#QBusiness.Paginator.ListIndices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listindicespaginator)
        """

class ListMessagesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listmessagespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListMessagesRequestListMessagesPaginateTypeDef]
    ) -> AsyncIterator[ListMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListMessages.html#QBusiness.Paginator.ListMessages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listmessagespaginator)
        """

class ListPluginActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginActionsRequestListPluginActionsPaginateTypeDef]
    ) -> AsyncIterator[ListPluginActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginActions.html#QBusiness.Paginator.ListPluginActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginactionspaginator)
        """

class ListPluginTypeActionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypeactionspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginTypeActionsRequestListPluginTypeActionsPaginateTypeDef]
    ) -> AsyncIterator[ListPluginTypeActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeActions.html#QBusiness.Paginator.ListPluginTypeActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypeactionspaginator)
        """

class ListPluginTypeMetadataPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypemetadatapaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginTypeMetadataRequestListPluginTypeMetadataPaginateTypeDef]
    ) -> AsyncIterator[ListPluginTypeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPluginTypeMetadata.html#QBusiness.Paginator.ListPluginTypeMetadata.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listplugintypemetadatapaginator)
        """

class ListPluginsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPluginsRequestListPluginsPaginateTypeDef]
    ) -> AsyncIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListPlugins.html#QBusiness.Paginator.ListPlugins.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listpluginspaginator)
        """

class ListRetrieversPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listretrieverspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListRetrieversRequestListRetrieversPaginateTypeDef]
    ) -> AsyncIterator[ListRetrieversResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListRetrievers.html#QBusiness.Paginator.ListRetrievers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listretrieverspaginator)
        """

class ListWebExperiencesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listwebexperiencespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListWebExperiencesRequestListWebExperiencesPaginateTypeDef]
    ) -> AsyncIterator[ListWebExperiencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/ListWebExperiences.html#QBusiness.Paginator.ListWebExperiences.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#listwebexperiencespaginator)
        """

class SearchRelevantContentPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#searchrelevantcontentpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchRelevantContentRequestSearchRelevantContentPaginateTypeDef]
    ) -> AsyncIterator[SearchRelevantContentResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/qbusiness/paginator/SearchRelevantContent.html#QBusiness.Paginator.SearchRelevantContent.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_qbusiness/paginators/#searchrelevantcontentpaginator)
        """

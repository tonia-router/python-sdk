# tonia_generated.MemberRuntimeApi

All URIs are relative to *https://pass.tonia.ca*

Method | HTTP request | Description
------------- | ------------- | -------------
[**conversations_append**](MemberRuntimeApi.md#conversations_append) | **POST** /v1/conversations/{conversation_id}/messages | Append messages to a conversation
[**conversations_create**](MemberRuntimeApi.md#conversations_create) | **POST** /v1/conversations | Create conversation
[**conversations_delete**](MemberRuntimeApi.md#conversations_delete) | **DELETE** /v1/conversations/{conversation_id} | Delete one conversation
[**conversations_delete_history**](MemberRuntimeApi.md#conversations_delete_history) | **DELETE** /v1/conversations | Bulk-delete all conversations for the member
[**conversations_export**](MemberRuntimeApi.md#conversations_export) | **GET** /v1/conversations/export | Loi 25 conversation export
[**conversations_get**](MemberRuntimeApi.md#conversations_get) | **GET** /v1/conversations/{conversation_id} | Get conversation with messages
[**conversations_list**](MemberRuntimeApi.md#conversations_list) | **GET** /v1/conversations | List conversations
[**conversations_update**](MemberRuntimeApi.md#conversations_update) | **PATCH** /v1/conversations/{conversation_id} | Archive / unarchive conversation


# **conversations_append**
> ConversationsAppend200Response conversations_append(conversation_id, conversation_append_request)

Append messages to a conversation

DLP/media denials always return hard HTTP 451 (no chat_200).

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_append_request import ConversationAppendRequest
from tonia_generated.models.conversations_append200_response import ConversationsAppend200Response
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    conversation_id = 'conversation_id_example' # str | 
    conversation_append_request = tonia_generated.ConversationAppendRequest() # ConversationAppendRequest | 

    try:
        # Append messages to a conversation
        api_response = api_instance.conversations_append(conversation_id, conversation_append_request)
        print("The response of MemberRuntimeApi->conversations_append:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_append: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversation_id** | **str**|  | 
 **conversation_append_request** | [**ConversationAppendRequest**](ConversationAppendRequest.md)|  | 

### Return type

[**ConversationsAppend200Response**](ConversationsAppend200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Append result |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_create**
> ConversationSummary conversations_create(conversation_create_request=conversation_create_request)

Create conversation

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_create_request import ConversationCreateRequest
from tonia_generated.models.conversation_summary import ConversationSummary
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    conversation_create_request = tonia_generated.ConversationCreateRequest() # ConversationCreateRequest |  (optional)

    try:
        # Create conversation
        api_response = api_instance.conversations_create(conversation_create_request=conversation_create_request)
        print("The response of MemberRuntimeApi->conversations_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversation_create_request** | [**ConversationCreateRequest**](ConversationCreateRequest.md)|  | [optional] 

### Return type

[**ConversationSummary**](ConversationSummary.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created conversation summary |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_delete**
> ConversationsDelete200Response conversations_delete(conversation_id)

Delete one conversation

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversations_delete200_response import ConversationsDelete200Response
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    conversation_id = 'conversation_id_example' # str | 

    try:
        # Delete one conversation
        api_response = api_instance.conversations_delete(conversation_id)
        print("The response of MemberRuntimeApi->conversations_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversation_id** | **str**|  | 

### Return type

[**ConversationsDelete200Response**](ConversationsDelete200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Deleted |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_delete_history**
> ConversationsDeleteHistory200Response conversations_delete_history()

Bulk-delete all conversations for the member

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversations_delete_history200_response import ConversationsDeleteHistory200Response
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)

    try:
        # Bulk-delete all conversations for the member
        api_response = api_instance.conversations_delete_history()
        print("The response of MemberRuntimeApi->conversations_delete_history:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_delete_history: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ConversationsDeleteHistory200Response**](ConversationsDeleteHistory200Response.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bulk delete result |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_export**
> ConversationExport conversations_export()

Loi 25 conversation export

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_export import ConversationExport
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)

    try:
        # Loi 25 conversation export
        api_response = api_instance.conversations_export()
        print("The response of MemberRuntimeApi->conversations_export:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_export: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ConversationExport**](ConversationExport.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Export payload |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_get**
> ConversationDetail conversations_get(conversation_id)

Get conversation with messages

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_detail import ConversationDetail
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    conversation_id = 'conversation_id_example' # str | 

    try:
        # Get conversation with messages
        api_response = api_instance.conversations_get(conversation_id)
        print("The response of MemberRuntimeApi->conversations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversation_id** | **str**|  | 

### Return type

[**ConversationDetail**](ConversationDetail.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversation detail |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_list**
> ConversationList conversations_list(archived=archived)

List conversations

Requires member-bound `app_session` key and `chat_history` entitlement.

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_list import ConversationList
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    archived = 56 # int | When `1`, list archived conversations (optional)

    try:
        # List conversations
        api_response = api_instance.conversations_list(archived=archived)
        print("The response of MemberRuntimeApi->conversations_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **archived** | **int**| When &#x60;1&#x60;, list archived conversations | [optional] 

### Return type

[**ConversationList**](ConversationList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Conversation summaries |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **conversations_update**
> ConversationSummary conversations_update(conversation_id, conversations_update_request)

Archive / unarchive conversation

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.conversation_summary import ConversationSummary
from tonia_generated.models.conversations_update_request import ConversationsUpdateRequest
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Configure Bearer authorization (tonia_*): BearerAuth
configuration = tonia_generated.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.MemberRuntimeApi(api_client)
    conversation_id = 'conversation_id_example' # str | 
    conversations_update_request = tonia_generated.ConversationsUpdateRequest() # ConversationsUpdateRequest | 

    try:
        # Archive / unarchive conversation
        api_response = api_instance.conversations_update(conversation_id, conversations_update_request)
        print("The response of MemberRuntimeApi->conversations_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MemberRuntimeApi->conversations_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **conversation_id** | **str**|  | 
 **conversations_update_request** | [**ConversationsUpdateRequest**](ConversationsUpdateRequest.md)|  | 

### Return type

[**ConversationSummary**](ConversationSummary.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Updated summary |  -  |
**0** | Conversations family error. No &#x60;retryable&#x60; field. Auth-missing body is type-only (no &#x60;code&#x60;). Policy denials are always hard 451 with a thinner body than runtime.  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


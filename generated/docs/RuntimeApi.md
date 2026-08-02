# tonia_generated.RuntimeApi

All URIs are relative to *https://pass.tonia.ca*

Method | HTTP request | Description
------------- | ------------- | -------------
[**chat_completions_create**](RuntimeApi.md#chat_completions_create) | **POST** /v1/chat/completions | OpenAI-shaped chat completions (passthrough)
[**embeddings_create**](RuntimeApi.md#embeddings_create) | **POST** /v1/embeddings | OpenAI-shaped embeddings (passthrough)
[**images_edit**](RuntimeApi.md#images_edit) | **POST** /v1/images/edits | OpenAI-shaped image edits (passthrough)
[**images_generate**](RuntimeApi.md#images_generate) | **POST** /v1/images/generations | OpenAI-shaped image generations (passthrough)
[**interactions_create**](RuntimeApi.md#interactions_create) | **POST** /v1/interactions | Gemini-shaped interactions (passthrough)
[**messages_create**](RuntimeApi.md#messages_create) | **POST** /v1/messages | Anthropic-shaped messages (passthrough)
[**models_get**](RuntimeApi.md#models_get) | **GET** /v1/models/{id} | Runtime model retrieve
[**models_list**](RuntimeApi.md#models_list) | **GET** /v1/models | Runtime model discovery for the calling key
[**rerank_create**](RuntimeApi.md#rerank_create) | **POST** /v1/rerank | Cohere-shaped rerank (passthrough)
[**responses_create**](RuntimeApi.md#responses_create) | **POST** /v1/responses | OpenAI Responses API (passthrough)


# **chat_completions_create**
> PassthroughOrBlockResponse chat_completions_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

OpenAI-shaped chat completions (passthrough)

Upstream-shaped body. Prefer `Authorization: Bearer`. May return HTTP
200 with `_tonia_policy_block` or `_tonia_entitlement_block` carriers —
SDKs must raise typed errors. Soft-limit headers `x-tonia-limit-*`
may appear on success. Top-level `reasoning_effort` is an untyped
passthrough field; Pass clamps to the model's declared set.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.passthrough_or_block_response import PassthroughOrBlockResponse
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # OpenAI-shaped chat completions (passthrough)
        api_response = api_instance.chat_completions_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->chat_completions_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->chat_completions_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

[**PassthroughOrBlockResponse**](PassthroughOrBlockResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native completion, or chat_200 block carrier |  * x-tonia-limit-warning -  <br>  * x-tonia-policy-block -  <br>  * x-tonia-entitlement-block -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **embeddings_create**
> Dict[str, object] embeddings_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

OpenAI-shaped embeddings (passthrough)

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # OpenAI-shaped embeddings (passthrough)
        api_response = api_instance.embeddings_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->embeddings_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->embeddings_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native embeddings response |  * x-tonia-limit-warning -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **images_edit**
> Dict[str, object] images_edit(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

OpenAI-shaped image edits (passthrough)

Pass may rebuild JSON→multipart before upstream. Policy/entitlement
denials are always hard HTTP on this surface.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # OpenAI-shaped image edits (passthrough)
        api_response = api_instance.images_edit(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->images_edit:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->images_edit: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native image edit response |  * x-tonia-limit-warning -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **images_generate**
> Dict[str, object] images_generate(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

OpenAI-shaped image generations (passthrough)

Policy/entitlement denials on this surface are always hard HTTP (no chat_200).

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # OpenAI-shaped image generations (passthrough)
        api_response = api_instance.images_generate(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->images_generate:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->images_generate: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native image response |  * x-tonia-limit-warning -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **interactions_create**
> Dict[str, object] interactions_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

Gemini-shaped interactions (passthrough)

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # Gemini-shaped interactions (passthrough)
        api_response = api_instance.interactions_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->interactions_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->interactions_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native interactions response |  * x-tonia-limit-warning -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **messages_create**
> PassthroughOrBlockResponse messages_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

Anthropic-shaped messages (passthrough)

Prefer `x-api-key`. Same chat_200 carrier / soft-limit rules as chat.

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.passthrough_or_block_response import PassthroughOrBlockResponse
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # Anthropic-shaped messages (passthrough)
        api_response = api_instance.messages_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->messages_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->messages_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

[**PassthroughOrBlockResponse**](PassthroughOrBlockResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native message, or chat_200 block carrier |  * x-tonia-limit-warning -  <br>  * x-tonia-policy-block -  <br>  * x-tonia-entitlement-block -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_get**
> RuntimeModel models_get(id, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

Runtime model retrieve

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.runtime_model import RuntimeModel
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    id = 'id_example' # str | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # Runtime model retrieve
        api_response = api_instance.models_get(id, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->models_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->models_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

[**RuntimeModel**](RuntimeModel.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Single runtime model entry |  -  |
**404** | Structured runtime error |  -  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_list**
> RuntimeModelList models_list(http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

Runtime model discovery for the calling key

Authenticated list scoped to what the key/tenant may call.
Header shape affects list presentation (`x-api-key` only → Anthropic-
shaped ids; Bearer → OpenAI-shaped). Optional `reasoning` descriptor
when the model declares efforts.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.runtime_model_list import RuntimeModelList
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # Runtime model discovery for the calling key
        api_response = api_instance.models_list(http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->models_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->models_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

[**RuntimeModelList**](RuntimeModelList.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Runtime model list |  -  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rerank_create**
> Dict[str, object] rerank_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

Cohere-shaped rerank (passthrough)

### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # Cohere-shaped rerank (passthrough)
        api_response = api_instance.rerank_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->rerank_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->rerank_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

**Dict[str, object]**

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native rerank response |  * x-tonia-limit-warning -  <br>  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **responses_create**
> PassthroughOrBlockResponse responses_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)

OpenAI Responses API (passthrough)

WebSocket upgrade on this path is refused with JSON HTTP 426
(`websocket_upgrade_unsupported`). Use HTTPS POST with `stream: true`
for SSE.


### Example

* Api Key Authentication (ApiKeyAuth):
* Bearer (tonia_*) Authentication (BearerAuth):

```python
import tonia_generated
from tonia_generated.models.passthrough_or_block_response import PassthroughOrBlockResponse
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
    api_instance = tonia_generated.RuntimeApi(api_client)
    request_body = None # Dict[str, object] | 
    http_referer = 'http_referer_example' # str | Optional app attribution (also accepts `Referer`). Never gates admission. (optional)
    x_tonia_title = 'x_tonia_title_example' # str | Optional app title (aliases `X-OpenRouter-Title`, `X-Title`). (optional)
    x_tonia_categories = 'x_tonia_categories_example' # str | Optional comma-separated categories (max 8). Alias `X-OpenRouter-Categories`. (optional)

    try:
        # OpenAI Responses API (passthrough)
        api_response = api_instance.responses_create(request_body, http_referer=http_referer, x_tonia_title=x_tonia_title, x_tonia_categories=x_tonia_categories)
        print("The response of RuntimeApi->responses_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RuntimeApi->responses_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **request_body** | [**Dict[str, object]**](object.md)|  | 
 **http_referer** | **str**| Optional app attribution (also accepts &#x60;Referer&#x60;). Never gates admission. | [optional] 
 **x_tonia_title** | **str**| Optional app title (aliases &#x60;X-OpenRouter-Title&#x60;, &#x60;X-Title&#x60;). | [optional] 
 **x_tonia_categories** | **str**| Optional comma-separated categories (max 8). Alias &#x60;X-OpenRouter-Categories&#x60;. | [optional] 

### Return type

[**PassthroughOrBlockResponse**](PassthroughOrBlockResponse.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth), [BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, text/event-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Provider-native Responses body, or chat_200 block carrier |  * x-tonia-limit-warning -  <br>  * x-tonia-policy-block -  <br>  * x-tonia-entitlement-block -  <br>  |
**426** | WebSocket upgrade refused (JSON body) |  -  |
**0** | Structured runtime error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


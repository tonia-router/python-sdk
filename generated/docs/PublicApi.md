# tonia_generated.PublicApi

All URIs are relative to *https://pass.tonia.ca*

Method | HTTP request | Description
------------- | ------------- | -------------
[**catalogue_list**](PublicApi.md#catalogue_list) | **GET** /v1/public/catalogue | Commercial tier / offer catalogue
[**public_model_categories_list**](PublicApi.md#public_model_categories_list) | **GET** /v1/public/model-categories | Category labels for the public model catalogue
[**public_models_get**](PublicApi.md#public_models_get) | **GET** /v1/public/models/{id} | Public Managed model SKU detail
[**public_models_list**](PublicApi.md#public_models_list) | **GET** /v1/public/models | Public Managed model SKU list
[**status_get**](PublicApi.md#status_get) | **GET** /v1/status | Public service health aggregation


# **catalogue_list**
> PublicCatalogue catalogue_list()

Commercial tier / offer catalogue

Unauthenticated commercial catalogue (Stripe products, public active
offers, entitlement templates). Not a model SKU list — use
`/v1/public/models` for Managed SKUs.


### Example


```python
import tonia_generated
from tonia_generated.models.public_catalogue import PublicCatalogue
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)


# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.PublicApi(api_client)

    try:
        # Commercial tier / offer catalogue
        api_response = api_instance.catalogue_list()
        print("The response of PublicApi->catalogue_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicApi->catalogue_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicCatalogue**](PublicCatalogue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Catalogue snapshot |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **public_model_categories_list**
> PublicModelCategoryList public_model_categories_list()

Category labels for the public model catalogue

### Example


```python
import tonia_generated
from tonia_generated.models.public_model_category_list import PublicModelCategoryList
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)


# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.PublicApi(api_client)

    try:
        # Category labels for the public model catalogue
        api_response = api_instance.public_model_categories_list()
        print("The response of PublicApi->public_model_categories_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicApi->public_model_categories_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicModelCategoryList**](PublicModelCategoryList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Active category definitions |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **public_models_get**
> PublicModelDetail public_models_get(id)

Public Managed model SKU detail

### Example


```python
import tonia_generated
from tonia_generated.models.public_model_detail import PublicModelDetail
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)


# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.PublicApi(api_client)
    id = 'id_example' # str | 

    try:
        # Public Managed model SKU detail
        api_response = api_instance.public_models_get(id)
        print("The response of PublicApi->public_models_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicApi->public_models_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**PublicModelDetail**](PublicModelDetail.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Public model detail (may include telemetry enrichment) |  -  |
**404** | Flat string error (not structured taxonomy) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **public_models_list**
> PublicModelList public_models_list()

Public Managed model SKU list

### Example


```python
import tonia_generated
from tonia_generated.models.public_model_list import PublicModelList
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)


# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.PublicApi(api_client)

    try:
        # Public Managed model SKU list
        api_response = api_instance.public_models_list()
        print("The response of PublicApi->public_models_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicApi->public_models_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicModelList**](PublicModelList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of public model details |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **status_get**
> PublicStatus status_get()

Public service health aggregation

### Example


```python
import tonia_generated
from tonia_generated.models.public_status import PublicStatus
from tonia_generated.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://pass.tonia.ca
# See configuration.py for a list of all supported configuration parameters.
configuration = tonia_generated.Configuration(
    host = "https://pass.tonia.ca"
)


# Enter a context with an instance of the API client
with tonia_generated.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tonia_generated.PublicApi(api_client)

    try:
        # Public service health aggregation
        api_response = api_instance.status_get()
        print("The response of PublicApi->status_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PublicApi->status_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PublicStatus**](PublicStatus.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Aggregated status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


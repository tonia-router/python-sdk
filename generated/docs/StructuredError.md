# StructuredError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**code** | **str** |  | [optional] 
**retryable** | **bool** | Present on runtime hard errors except policy_block | [optional] 
**scope** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**provider** | **str** |  | [optional] 
**detail** | **str** |  | [optional] 
**docs** | **str** |  | [optional] 
**law25_article** | **str** |  | [optional] 
**efvp_section** | **str** |  | [optional] 
**scope_field** | **str** |  | [optional] 
**requested** | **str** |  | [optional] 
**allowed** | **str** |  | [optional] 
**status** | **int** |  | [optional] 
**dlp** | **Dict[str, object]** |  | [optional] 
**media** | **Dict[str, object]** |  | [optional] 

## Example

```python
from tonia_generated.models.structured_error import StructuredError

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredError from a JSON string
structured_error_instance = StructuredError.from_json(json)
# print the JSON string representation of the object
print(StructuredError.to_json())

# convert the object into a dict
structured_error_dict = structured_error_instance.to_dict()
# create an instance of StructuredError from a dict
structured_error_from_dict = StructuredError.from_dict(structured_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# RuntimeModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**object** | **str** |  | 
**context_length** | **int** |  | 
**supported_parameters** | **List[str]** |  | 
**capabilities** | **List[str]** |  | [optional] 
**reasoning** | [**ReasoningDescriptor**](ReasoningDescriptor.md) |  | [optional] 
**pricing** | **Dict[str, object]** | Present for managed-priced models only | [optional] 

## Example

```python
from tonia_generated.models.runtime_model import RuntimeModel

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeModel from a JSON string
runtime_model_instance = RuntimeModel.from_json(json)
# print the JSON string representation of the object
print(RuntimeModel.to_json())

# convert the object into a dict
runtime_model_dict = runtime_model_instance.to_dict()
# create an instance of RuntimeModel from a dict
runtime_model_from_dict = RuntimeModel.from_dict(runtime_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



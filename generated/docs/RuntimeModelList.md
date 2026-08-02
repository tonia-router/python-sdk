# RuntimeModelList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  | 
**data** | [**List[RuntimeModel]**](RuntimeModel.md) |  | 

## Example

```python
from tonia_generated.models.runtime_model_list import RuntimeModelList

# TODO update the JSON string below
json = "{}"
# create an instance of RuntimeModelList from a JSON string
runtime_model_list_instance = RuntimeModelList.from_json(json)
# print the JSON string representation of the object
print(RuntimeModelList.to_json())

# convert the object into a dict
runtime_model_list_dict = runtime_model_list_instance.to_dict()
# create an instance of RuntimeModelList from a dict
runtime_model_list_from_dict = RuntimeModelList.from_dict(runtime_model_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



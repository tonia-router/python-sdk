# ReasoningDescriptor

tonia-native per-model reasoning effort descriptor

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**efforts** | **List[str]** | Declared effort labels for this model | 
**default** | **str** | Default effort when the client omits reasoning_effort | 

## Example

```python
from tonia_generated.models.reasoning_descriptor import ReasoningDescriptor

# TODO update the JSON string below
json = "{}"
# create an instance of ReasoningDescriptor from a JSON string
reasoning_descriptor_instance = ReasoningDescriptor.from_json(json)
# print the JSON string representation of the object
print(ReasoningDescriptor.to_json())

# convert the object into a dict
reasoning_descriptor_dict = reasoning_descriptor_instance.to_dict()
# create an instance of ReasoningDescriptor from a dict
reasoning_descriptor_from_dict = ReasoningDescriptor.from_dict(reasoning_descriptor_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



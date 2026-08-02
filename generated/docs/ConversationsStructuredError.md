# ConversationsStructuredError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**ConversationsStructuredErrorError**](ConversationsStructuredErrorError.md) |  | 

## Example

```python
from tonia_generated.models.conversations_structured_error import ConversationsStructuredError

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationsStructuredError from a JSON string
conversations_structured_error_instance = ConversationsStructuredError.from_json(json)
# print the JSON string representation of the object
print(ConversationsStructuredError.to_json())

# convert the object into a dict
conversations_structured_error_dict = conversations_structured_error_instance.to_dict()
# create an instance of ConversationsStructuredError from a dict
conversations_structured_error_from_dict = ConversationsStructuredError.from_dict(conversations_structured_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



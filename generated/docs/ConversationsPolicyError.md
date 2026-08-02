# ConversationsPolicyError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**ConversationsPolicyErrorError**](ConversationsPolicyErrorError.md) |  | 

## Example

```python
from tonia_generated.models.conversations_policy_error import ConversationsPolicyError

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationsPolicyError from a JSON string
conversations_policy_error_instance = ConversationsPolicyError.from_json(json)
# print the JSON string representation of the object
print(ConversationsPolicyError.to_json())

# convert the object into a dict
conversations_policy_error_dict = conversations_policy_error_instance.to_dict()
# create an instance of ConversationsPolicyError from a dict
conversations_policy_error_from_dict = ConversationsPolicyError.from_dict(conversations_policy_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



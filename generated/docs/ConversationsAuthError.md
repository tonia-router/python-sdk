# ConversationsAuthError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**ConversationsAuthErrorError**](ConversationsAuthErrorError.md) |  | 

## Example

```python
from tonia_generated.models.conversations_auth_error import ConversationsAuthError

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationsAuthError from a JSON string
conversations_auth_error_instance = ConversationsAuthError.from_json(json)
# print the JSON string representation of the object
print(ConversationsAuthError.to_json())

# convert the object into a dict
conversations_auth_error_dict = conversations_auth_error_instance.to_dict()
# create an instance of ConversationsAuthError from a dict
conversations_auth_error_from_dict = ConversationsAuthError.from_dict(conversations_auth_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



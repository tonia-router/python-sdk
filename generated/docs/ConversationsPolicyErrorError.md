# ConversationsPolicyErrorError

Thinner than runtime policy_block (no detail/efvp/status/dlp/media)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**code** | **str** |  | 
**law25_article** | **str** |  | [optional] 
**scope_field** | **str** |  | [optional] 
**requested** | **str** |  | [optional] 
**allowed** | **str** |  | [optional] 

## Example

```python
from tonia_generated.models.conversations_policy_error_error import ConversationsPolicyErrorError

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationsPolicyErrorError from a JSON string
conversations_policy_error_error_instance = ConversationsPolicyErrorError.from_json(json)
# print the JSON string representation of the object
print(ConversationsPolicyErrorError.to_json())

# convert the object into a dict
conversations_policy_error_error_dict = conversations_policy_error_error_instance.to_dict()
# create an instance of ConversationsPolicyErrorError from a dict
conversations_policy_error_error_from_dict = ConversationsPolicyErrorError.from_dict(conversations_policy_error_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



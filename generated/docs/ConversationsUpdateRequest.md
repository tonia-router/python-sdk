# ConversationsUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived** | **bool** |  | 

## Example

```python
from tonia_generated.models.conversations_update_request import ConversationsUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationsUpdateRequest from a JSON string
conversations_update_request_instance = ConversationsUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(ConversationsUpdateRequest.to_json())

# convert the object into a dict
conversations_update_request_dict = conversations_update_request_instance.to_dict()
# create an instance of ConversationsUpdateRequest from a dict
conversations_update_request_from_dict = ConversationsUpdateRequest.from_dict(conversations_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



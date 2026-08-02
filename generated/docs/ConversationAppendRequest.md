# ConversationAppendRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**messages** | **List[Dict[str, object]]** |  | 

## Example

```python
from tonia_generated.models.conversation_append_request import ConversationAppendRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationAppendRequest from a JSON string
conversation_append_request_instance = ConversationAppendRequest.from_json(json)
# print the JSON string representation of the object
print(ConversationAppendRequest.to_json())

# convert the object into a dict
conversation_append_request_dict = conversation_append_request_instance.to_dict()
# create an instance of ConversationAppendRequest from a dict
conversation_append_request_from_dict = ConversationAppendRequest.from_dict(conversation_append_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



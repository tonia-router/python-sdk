# ConversationCreateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**messages** | **List[Dict[str, object]]** |  | [optional] 

## Example

```python
from tonia_generated.models.conversation_create_request import ConversationCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationCreateRequest from a JSON string
conversation_create_request_instance = ConversationCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ConversationCreateRequest.to_json())

# convert the object into a dict
conversation_create_request_dict = conversation_create_request_instance.to_dict()
# create an instance of ConversationCreateRequest from a dict
conversation_create_request_from_dict = ConversationCreateRequest.from_dict(conversation_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



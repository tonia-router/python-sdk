# ConversationDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**conversation_id** | **str** |  | 
**title** | **str** |  | 
**model** | **str** |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 
**message_count** | **int** |  | 
**archived_at** | **str** |  | 
**messages** | [**List[ConversationDetailAllOfMessages]**](ConversationDetailAllOfMessages.md) |  | 

## Example

```python
from tonia_generated.models.conversation_detail import ConversationDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationDetail from a JSON string
conversation_detail_instance = ConversationDetail.from_json(json)
# print the JSON string representation of the object
print(ConversationDetail.to_json())

# convert the object into a dict
conversation_detail_dict = conversation_detail_instance.to_dict()
# create an instance of ConversationDetail from a dict
conversation_detail_from_dict = ConversationDetail.from_dict(conversation_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



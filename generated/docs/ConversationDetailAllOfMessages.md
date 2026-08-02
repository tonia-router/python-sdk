# ConversationDetailAllOfMessages


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seq** | **int** |  | 
**role** | **str** |  | 
**content** | **str** |  | 
**attachments** | **List[Dict[str, object]]** |  | 
**created_at** | **str** |  | 

## Example

```python
from tonia_generated.models.conversation_detail_all_of_messages import ConversationDetailAllOfMessages

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationDetailAllOfMessages from a JSON string
conversation_detail_all_of_messages_instance = ConversationDetailAllOfMessages.from_json(json)
# print the JSON string representation of the object
print(ConversationDetailAllOfMessages.to_json())

# convert the object into a dict
conversation_detail_all_of_messages_dict = conversation_detail_all_of_messages_instance.to_dict()
# create an instance of ConversationDetailAllOfMessages from a dict
conversation_detail_all_of_messages_from_dict = ConversationDetailAllOfMessages.from_dict(conversation_detail_all_of_messages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# ConversationExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tenant_id** | **str** |  | 
**member_id** | **str** |  | 
**exported_at** | **str** |  | 
**conversations** | **List[Dict[str, object]]** |  | 

## Example

```python
from tonia_generated.models.conversation_export import ConversationExport

# TODO update the JSON string below
json = "{}"
# create an instance of ConversationExport from a JSON string
conversation_export_instance = ConversationExport.from_json(json)
# print the JSON string representation of the object
print(ConversationExport.to_json())

# convert the object into a dict
conversation_export_dict = conversation_export_instance.to_dict()
# create an instance of ConversationExport from a dict
conversation_export_from_dict = ConversationExport.from_dict(conversation_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



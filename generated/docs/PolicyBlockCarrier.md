# PolicyBlockCarrier

chat_200 policy block carrier (no retryable)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | 
**law25_article** | **str** |  | [optional] 
**efvp_section** | **str** |  | [optional] 
**scope_field** | **str** |  | [optional] 
**detail** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**action** | **str** |  | [optional] 
**categories** | **List[str]** |  | [optional] 
**hit_count** | **int** |  | [optional] 
**details** | **List[Dict[str, object]]** |  | [optional] 
**media** | **Dict[str, object]** |  | [optional] 

## Example

```python
from tonia_generated.models.policy_block_carrier import PolicyBlockCarrier

# TODO update the JSON string below
json = "{}"
# create an instance of PolicyBlockCarrier from a JSON string
policy_block_carrier_instance = PolicyBlockCarrier.from_json(json)
# print the JSON string representation of the object
print(PolicyBlockCarrier.to_json())

# convert the object into a dict
policy_block_carrier_dict = policy_block_carrier_instance.to_dict()
# create an instance of PolicyBlockCarrier from a dict
policy_block_carrier_from_dict = PolicyBlockCarrier.from_dict(policy_block_carrier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



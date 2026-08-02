# EntitlementBlockCarrier

chat_200 entitlement block carrier

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**code** | **str** |  | 
**scope** | **str** |  | 
**retryable** | **bool** |  | 
**message** | **str** |  | 
**action** | **str** |  | 

## Example

```python
from tonia_generated.models.entitlement_block_carrier import EntitlementBlockCarrier

# TODO update the JSON string below
json = "{}"
# create an instance of EntitlementBlockCarrier from a JSON string
entitlement_block_carrier_instance = EntitlementBlockCarrier.from_json(json)
# print the JSON string representation of the object
print(EntitlementBlockCarrier.to_json())

# convert the object into a dict
entitlement_block_carrier_dict = entitlement_block_carrier_instance.to_dict()
# create an instance of EntitlementBlockCarrier from a dict
entitlement_block_carrier_from_dict = EntitlementBlockCarrier.from_dict(entitlement_block_carrier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



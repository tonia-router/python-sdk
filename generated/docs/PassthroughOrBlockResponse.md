# PassthroughOrBlockResponse

Provider-native body. When policy/entitlement blocks render as chat_200, the same body also carries `_tonia_policy_block` or `_tonia_entitlement_block` — SDKs must detect and raise. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tonia_policy_block** | [**PolicyBlockCarrier**](PolicyBlockCarrier.md) |  | [optional] 
**tonia_entitlement_block** | [**EntitlementBlockCarrier**](EntitlementBlockCarrier.md) |  | [optional] 

## Example

```python
from tonia_generated.models.passthrough_or_block_response import PassthroughOrBlockResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PassthroughOrBlockResponse from a JSON string
passthrough_or_block_response_instance = PassthroughOrBlockResponse.from_json(json)
# print the JSON string representation of the object
print(PassthroughOrBlockResponse.to_json())

# convert the object into a dict
passthrough_or_block_response_dict = passthrough_or_block_response_instance.to_dict()
# create an instance of PassthroughOrBlockResponse from a dict
passthrough_or_block_response_from_dict = PassthroughOrBlockResponse.from_dict(passthrough_or_block_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



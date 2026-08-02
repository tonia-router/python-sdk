# PublicStatusComponentsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**status** | **str** |  | 
**detail** | **str** |  | 
**checked_at** | **str** |  | 
**public** | **bool** |  | 

## Example

```python
from tonia_generated.models.public_status_components_inner import PublicStatusComponentsInner

# TODO update the JSON string below
json = "{}"
# create an instance of PublicStatusComponentsInner from a JSON string
public_status_components_inner_instance = PublicStatusComponentsInner.from_json(json)
# print the JSON string representation of the object
print(PublicStatusComponentsInner.to_json())

# convert the object into a dict
public_status_components_inner_dict = public_status_components_inner_instance.to_dict()
# create an instance of PublicStatusComponentsInner from a dict
public_status_components_inner_from_dict = PublicStatusComponentsInner.from_dict(public_status_components_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



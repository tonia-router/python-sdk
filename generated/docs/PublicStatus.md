# PublicStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service** | **str** |  | 
**status** | **str** |  | 
**checked_at** | **datetime** |  | 
**components** | [**List[PublicStatusComponentsInner]**](PublicStatusComponentsInner.md) |  | 

## Example

```python
from tonia_generated.models.public_status import PublicStatus

# TODO update the JSON string below
json = "{}"
# create an instance of PublicStatus from a JSON string
public_status_instance = PublicStatus.from_json(json)
# print the JSON string representation of the object
print(PublicStatus.to_json())

# convert the object into a dict
public_status_dict = public_status_instance.to_dict()
# create an instance of PublicStatus from a dict
public_status_from_dict = PublicStatus.from_dict(public_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



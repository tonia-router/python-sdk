# PublicModelList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  | 
**data** | [**List[PublicModelDetail]**](PublicModelDetail.md) |  | 

## Example

```python
from tonia_generated.models.public_model_list import PublicModelList

# TODO update the JSON string below
json = "{}"
# create an instance of PublicModelList from a JSON string
public_model_list_instance = PublicModelList.from_json(json)
# print the JSON string representation of the object
print(PublicModelList.to_json())

# convert the object into a dict
public_model_list_dict = public_model_list_instance.to_dict()
# create an instance of PublicModelList from a dict
public_model_list_from_dict = PublicModelList.from_dict(public_model_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



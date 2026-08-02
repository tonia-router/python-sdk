# PublicModelDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**provider** | **str** |  | 
**display_name** | **str** |  | 
**object** | **str** |  | 
**description** | **str** |  | [optional] 
**description_fr** | **str** |  | [optional] 
**best_for** | **str** |  | [optional] 
**best_for_fr** | **str** |  | [optional] 
**categories** | **List[str]** |  | 
**context_length** | **int** |  | [optional] 
**release_date** | **str** |  | [optional] 
**modalities** | **Dict[str, object]** |  | [optional] 
**capabilities** | **List[str]** |  | 
**supported_parameters** | **List[str]** |  | 
**channel** | **str** |  | 
**status_component** | **str** |  | 
**reasoning** | [**ReasoningDescriptor**](ReasoningDescriptor.md) |  | [optional] 
**pricing** | **Dict[str, object]** |  | 
**performance** | **Dict[str, object]** |  | [optional] 
**uptime** | **Dict[str, object]** |  | [optional] 
**activity** | **Dict[str, object]** |  | [optional] 
**tools** | **Dict[str, object]** |  | [optional] 

## Example

```python
from tonia_generated.models.public_model_detail import PublicModelDetail

# TODO update the JSON string below
json = "{}"
# create an instance of PublicModelDetail from a JSON string
public_model_detail_instance = PublicModelDetail.from_json(json)
# print the JSON string representation of the object
print(PublicModelDetail.to_json())

# convert the object into a dict
public_model_detail_dict = public_model_detail_instance.to_dict()
# create an instance of PublicModelDetail from a dict
public_model_detail_from_dict = PublicModelDetail.from_dict(public_model_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



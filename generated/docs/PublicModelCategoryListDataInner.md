# PublicModelCategoryListDataInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**label_en** | **str** |  | 
**label_fr** | **str** |  | 
**sort_order** | **int** |  | 
**tone** | **str** |  | 

## Example

```python
from tonia_generated.models.public_model_category_list_data_inner import PublicModelCategoryListDataInner

# TODO update the JSON string below
json = "{}"
# create an instance of PublicModelCategoryListDataInner from a JSON string
public_model_category_list_data_inner_instance = PublicModelCategoryListDataInner.from_json(json)
# print the JSON string representation of the object
print(PublicModelCategoryListDataInner.to_json())

# convert the object into a dict
public_model_category_list_data_inner_dict = public_model_category_list_data_inner_instance.to_dict()
# create an instance of PublicModelCategoryListDataInner from a dict
public_model_category_list_data_inner_from_dict = PublicModelCategoryListDataInner.from_dict(public_model_category_list_data_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# PublicModelCategoryList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**object** | **str** |  | 
**data** | [**List[PublicModelCategoryListDataInner]**](PublicModelCategoryListDataInner.md) |  | 

## Example

```python
from tonia_generated.models.public_model_category_list import PublicModelCategoryList

# TODO update the JSON string below
json = "{}"
# create an instance of PublicModelCategoryList from a JSON string
public_model_category_list_instance = PublicModelCategoryList.from_json(json)
# print the JSON string representation of the object
print(PublicModelCategoryList.to_json())

# convert the object into a dict
public_model_category_list_dict = public_model_category_list_instance.to_dict()
# create an instance of PublicModelCategoryList from a dict
public_model_category_list_from_dict = PublicModelCategoryList.from_dict(public_model_category_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



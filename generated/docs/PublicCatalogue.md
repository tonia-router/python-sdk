# PublicCatalogue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**catalogue_version** | **str** |  | 
**catalogue_hash** | **str** |  | 
**products** | [**List[CatalogueProduct]**](CatalogueProduct.md) |  | 

## Example

```python
from tonia_generated.models.public_catalogue import PublicCatalogue

# TODO update the JSON string below
json = "{}"
# create an instance of PublicCatalogue from a JSON string
public_catalogue_instance = PublicCatalogue.from_json(json)
# print the JSON string representation of the object
print(PublicCatalogue.to_json())

# convert the object into a dict
public_catalogue_dict = public_catalogue_instance.to_dict()
# create an instance of PublicCatalogue from a dict
public_catalogue_from_dict = PublicCatalogue.from_dict(public_catalogue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



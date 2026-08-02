# CatalogueProduct


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_id** | **str** |  | 
**label** | **str** |  | 
**stripe_product_lookup_key** | **str** |  | 
**offers** | [**List[CatalogueOffer]**](CatalogueOffer.md) |  | 

## Example

```python
from tonia_generated.models.catalogue_product import CatalogueProduct

# TODO update the JSON string below
json = "{}"
# create an instance of CatalogueProduct from a JSON string
catalogue_product_instance = CatalogueProduct.from_json(json)
# print the JSON string representation of the object
print(CatalogueProduct.to_json())

# convert the object into a dict
catalogue_product_dict = catalogue_product_instance.to_dict()
# create an instance of CatalogueProduct from a dict
catalogue_product_from_dict = CatalogueProduct.from_dict(catalogue_product_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



# CatalogueOffer


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offer_id** | **str** |  | 
**product_id** | **str** |  | 
**status** | **str** |  | 
**label** | **str** |  | 
**credential_mode** | **str** |  | 
**public** | **bool** |  | 
**trial** | **Dict[str, object]** |  | 
**entitlement_template** | **Dict[str, object]** |  | 
**components** | **List[Dict[str, object]]** |  | 
**discounts** | **Dict[str, object]** |  | 
**managed_credit_topup_amounts_cad_cents** | **List[int]** |  | [optional] 

## Example

```python
from tonia_generated.models.catalogue_offer import CatalogueOffer

# TODO update the JSON string below
json = "{}"
# create an instance of CatalogueOffer from a JSON string
catalogue_offer_instance = CatalogueOffer.from_json(json)
# print the JSON string representation of the object
print(CatalogueOffer.to_json())

# convert the object into a dict
catalogue_offer_dict = catalogue_offer_instance.to_dict()
# create an instance of CatalogueOffer from a dict
catalogue_offer_from_dict = CatalogueOffer.from_dict(catalogue_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



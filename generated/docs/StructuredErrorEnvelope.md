# StructuredErrorEnvelope


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | [**StructuredError**](StructuredError.md) |  | 

## Example

```python
from tonia_generated.models.structured_error_envelope import StructuredErrorEnvelope

# TODO update the JSON string below
json = "{}"
# create an instance of StructuredErrorEnvelope from a JSON string
structured_error_envelope_instance = StructuredErrorEnvelope.from_json(json)
# print the JSON string representation of the object
print(StructuredErrorEnvelope.to_json())

# convert the object into a dict
structured_error_envelope_dict = structured_error_envelope_instance.to_dict()
# create an instance of StructuredErrorEnvelope from a dict
structured_error_envelope_from_dict = StructuredErrorEnvelope.from_dict(structured_error_envelope_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



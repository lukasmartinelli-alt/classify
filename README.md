# classilang
A DSL for [classifications](https://en.wikipedia.org/wiki/Classification) of objects.
This is targeted at classifications that require alot of constant and human entered data and not
fancy algorithms.

> **Goal**: Map a complex object to a single value based on constraints

## Operators

Operator | Description                                                            
---------|------------------------------------------------------------------------
$        | References a existing field from `data` or a constant from `constants`                
@>       | Value is contained in a list of values                                 
+	       | Addition
-	       | Subtraction
*	       | Multiplication
/	       | Division (integer division truncates the result)
%	       | Modulo (remainder)
^	       | Exponentiation

## Examples

### Tax Classification

Classify people into three tax classes.

```yaml
data:
  - income
constants:
  upper_threshold: 120000
  lower_threshold:  50000
classify:
  tax_rate:
    20.3: $income < $lower_threshold
    25.8: $income > $lower_threshold && $income < $upper_threshold
    35.1: $income > $upper_threshold
```


### OpenStreetMap Tags

In our OpenStreetMap project [osm2vectortiles](github.com/osm2vectortiles/osm2vectortiles)
we classify various OpenStreetMap tags into a `feature_class` to allow designers to easily
style groups of values.

```yaml
data:
  - key
  - value
constants:
  main_values:
    - primary
    - primary_link
    - trunk
    - trunk_link
    - secondary
    - secondary_link
    - tertiary
    - tertiary_link
  street_values:
    - residential
    - unclassified
    - living_street
    - road
    - raceway
classify:
  feature_class:
    driveway: $value == driveway
    main:     $value <@ $main_values
    street:   $value <@ $street_values
  color:
    orange:   $key == road || $key == way
    blue:     $key == water <@ $main_values
```

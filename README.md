# classilang
A DSL for [classifications](https://en.wikipedia.org/wiki/Classification) of objects.
This is targeted at classifications that require alot of constant and human entered data and not
fancy algorithms.

> **Goal**: Map a complex object to a single value based on constraints

## Operators

Operator | Description
---------|------------------------------------------------------------------------
`$`      | References a existing field from `data` or a constant from `constants`
`@>`     | Value is contained in a list of values
`+`      | Addition
`-`	     | Subtraction
`*`	     | Multiplication
`/`	     | Division (integer division truncates the result)
`%`	     | Modulo (remainder)
`^`	     | Exponentiation

## Examples

### Motion Picture Rating

Classify films with regard to suitability for audiences.

```javascript
system movie_ratings_children {
    object {
      age: Integer
      country: String
    }

    $country == argentinia {
        class ATP: $age > 0
        class 13: $age >= 13
        class 16: $age >= 16
        class 18: $age >= 18
        class "18, conditional display": $age >= 18
    }

    $country == australia {
        class PG: $age > 0
        class G: $age > 0
        class MA15+: $age >= 15
        class M: $age >= 15
        class R18: $age >= 18
        class X18+: $age >= 18
    }
}
```

### Tax Classification

Classify people into three tax classes.

```javascript
const upper_threshold: 120000
const lower_threshold:  50000

system tax_burden_income {
    object {
      income: Float
    }
    class 20.3: $income < $lower_thresholk
    class 25.8: $income > $lower_threshold && $income < $upper_threshold
    class 35.1: $income > $upper_threshold
}
```

Generated code.

```python
def tax_burden_income(income):
    upper_threshold = 120000
    lower_threshold =  50000
    if income < lower_threshold:
        yield 20.3
    if income < lower_threshold and income < upper_threshold>:
        yield 20.3
    if income > upper_threshold>:
        yield 35.1
```


### OpenStreetMap Tags

In our OpenStreetMap project [osm2vectortiles](github.com/osm2vectortiles/osm2vectortiles)
we classify various OpenStreetMap tags into a `feature_class` to allow designers to easily
style groups of values.

```javascript
const main_values {
    primary
    primary_link
    trunk
    trunk_link
    secondary
    secondary_link
    tertiary
    tertiary_link
}

const street_values {
    residential
    unclassified
    living_street
    road
    raceway
}

system osm_feature_class {
    object osm_tag {
      key: String
      value: String
    }

    $key == road {
        class driveway: $value == driveway
        class main:     $value <@ $main_values
        class street:   $value <@ $street_values
    }
}
```

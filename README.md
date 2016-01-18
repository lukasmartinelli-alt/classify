# classify

A YAML format for [classification](https://en.wikipedia.org/wiki/Classification) of scalar values.
A Python compiler will produce a classification function in `Python` and `SQL`
for the given YAML format.

This approach is for the use case in [osm2vectortiles](github.com/osm2vectortiles/osm2vectortiles)
where many values need to be reduced to a single value.

![Classification of many values](classification.png)

## Example

This maps the value of a OpenStreetMap tag into a `feature_class`. This enables map designers
to style several map features at once (e.g. the `main` roads instead of alot of individual road types).

Create a new file `feature_class.yml` and name your classification system.
Then you need to list all classes you want to reduce (`street`, `main`, `driveway`).
For each class you define a list of values that you want to map to your class.

```javascript
system:
  name: OSM Feature Class
  classes:
    street:
    - residential
    - unclassified
    - living_street
    - road
    - raceway
    main:
    - primary
    - primary_link
    - trunk
    - trunk_link
    - secondary
    - secondary_link
    - tertiary
    - tertiary_link
    driveway:
    - driveway
```

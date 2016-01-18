# classify [![Build Status](https://travis-ci.org/lukasmartinelli/classify.svg?branch=master)](https://travis-ci.org/lukasmartinelli/classify) [![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://tldrlegal.com/license/mit-license)

<img align="right" alt="Classification of many values" src="classification.png" />

A YAML format for [classification](https://en.wikipedia.org/wiki/Classification) of single values.
The `classify.py` Python program will produce a classification function for various language targets
for the given YAML format.

This approach is used in [osm2vectortiles](github.com/osm2vectortiles/osm2vectortiles)
where we categorize OpenStreetMap values into different feature classes and icons.

## Get started

You need to have Python 2 or Python 3 installed on your system.

```
git clone https://github.com/lukasmartinelli/classify.git
cd classify
pip install -r requirements.txt

# generate sql code
./classify.py sql <yaml-definition>

# generate python code
./classify.py python <yaml-definition>
```

## Example

Map the value of a OpenStreetMap tag into a `feature_class`. This enables map designers
to style several map features at once (e.g. the `main` roads instead of alot of individual road types).

Create a new file `feature_class.yml` and name your classification system.
Then you need to list all classes you want to reduce (`street`, `main`, `driveway`).
For each class you define a list of values that you want to map to your class.

```yml
system:
  name: feature_class
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

Generated SQL.

```sql
CREATE OR REPLACE FUNCTION classify_osm_feature_class(type VARCHAR)
  RETURNS VARCHAR AS $$
  BEGIN
  RETURN CASE
    WHEN type IN ('motorway','motorway_link','driveway') THEN 'highway'
    WHEN type IN ('primary','primary_link', 'trunk', 'trunk_link',
                  'secondary','secondary_link',
                  'tertiary','tertiary_link') THEN 'main'
  END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

## Structure

The `system` defines a classification system for values. You can give a system
a `name`. The name of your `system` will appear in the generated code.

A classification system has many `classes`. Each class is a key (the class name) and
values (the values that are matched to the class). Only text values are supported.

```yml
system:
  name: <name-classification-system>
  classes:
    <class-name>:
    - <value-to-match>
```

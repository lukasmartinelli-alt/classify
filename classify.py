#!/usr/bin/env python
"""Generate classification functions from custom YAML mapping
Usage:
  classify.py sql <yaml-source>
  classify.py python <yaml-source>
  classify.py javascript <yaml-source>
  classify.py (-h | --help)
Options:
  -h --help                 Show this screen.
  --version                 Show version.
"""
from collections import namedtuple
from docopt import docopt
import yaml


Class = namedtuple('Class', ['name', 'values'])


def generate_javascript(source):
    def generate_if_statement(class_name, mapping_values):
        value_strings = ["'{}'".format(value) for value in mapping_values]
        return (
            ' ' * 4 + "if([{0}].indexOf(value) > -1) {{ return '{1}'; }}"
        ).format(', '.join(value_strings), class_name)

    system_name = source['system']['name']
    classes = find_classes(source)
    if_statements = [generate_if_statement(cl, val) for cl, val in classes]

    return 'function classify_{0}(value) {{\n{1}\n}}'.format(
        system_name,
        '\n'.join(if_statements)
    )


def generate_python(source):
    def generate_if_statement(class_name, mapping_values):
        value_strings = ["'{}'".format(value) for value in mapping_values]
        return (
            ' ' * 4 + 'if value in [{0}]:\n' +
            ' ' * 8 + "return '{1}'"
        ).format(','.join(value_strings), class_name)

    system_name = source['system']['name']
    classes = find_classes(source)
    if_statements = [generate_if_statement(cl, val) for cl, val in classes]

    return 'def classify_{0}(value):\n{1}'.format(system_name,
                                                  '\n'.join(if_statements))


def generate_sql(source):
    def generate_when_statement(class_name, mapping_values):
        in_statements = ["'{}'".format(value) for value in mapping_values]
        return " " * 12 + "WHEN type IN ({0}) THEN '{1}'".format(
            ','.join(in_statements),
            class_name
        )

    system_name = source['system']['name']
    classes = find_classes(source)

    when_statements = [generate_when_statement(cl, val) for cl, val in classes]

    return """CREATE OR REPLACE FUNCTION classify_{0}(type VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    RETURN CASE
{1}
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
    """.format(system_name, "\n".join(when_statements))


def find_classes(config):
    for cl_name, mapped_values in config['system']['classes'].items():
        yield Class(cl_name, mapped_values)


if __name__ == '__main__':
    args = docopt(__doc__)

    with open(args['<yaml-source>'], 'r') as f:
        source = yaml.load(f)
        if args['sql']:
            print(generate_sql(source))
        if args['python']:
            print(generate_python(source))
        if args['javascript']:
            print(generate_javascript(source))

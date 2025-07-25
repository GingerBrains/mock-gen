import click
from .schema import parse_schema
from .core import generate_data
from .formats.json_writer import write_json
from .formats.csv_writer import write_csv
from .formats.sql_writer import write_sql
import json
import os
import random
from faker import Faker

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')

@click.command()
@click.option('--format', type=click.Choice(['json', 'csv', 'sql']), default='json', help='Output format')
@click.option('--count', type=int, default=None, help='Number of records to generate (will prompt if not provided)')
@click.option('--schema', type=str, required=False, help='Schema definition (JSON string)')
@click.option('--schema-file', type=click.Path(exists=True), required=False, help='Path to schema JSON file')
@click.option('--template', type=str, required=False, help='Name of built-in template in templates/ directory (e.g., user)')
@click.option('--output', type=click.Path(), default=None, help='Output file (defaults to stdout)')
@click.option('--seed', type=int, required=False, help='Set random seed for deterministic output')
def generate(format, count, schema, schema_file, template, output, seed):
    """Generate test data based on the provided schema or template."""
    # Set seed if provided
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)
    # Load schema from file, template, or string
    if schema_file:
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_str = f.read()
        except Exception as e:
            click.echo(f'Error reading schema file: {e}', err=True)
            return
    elif template:
        template_path = os.path.join(TEMPLATES_DIR, f'{template}.json')
        if not os.path.exists(template_path):
            click.echo(f'Template not found: {template_path}', err=True)
            return
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                schema_str = f.read()
        except Exception as e:
            click.echo(f'Error reading template file: {e}', err=True)
            return
    elif schema:
        schema_str = schema
    else:
        click.echo('Error: You must provide --schema, --schema-file, or --template.', err=True)
        return
    # Parse schema
    try:
        parsed_schema = parse_schema(schema_str)
    except Exception as e:
        click.echo(f'Error parsing schema: {e}', err=True)
        return
    # Prompt for count if not provided
    if count is None:
        count = click.prompt('How many records do you want to generate?', type=int)
    # Generate data
    try:
        data = generate_data(parsed_schema, count)
    except Exception as e:
        click.echo(f'Error generating data: {e}', err=True)
        return
    # Output
    if format == 'json':
        write_json(data, output_file=output)
    elif format == 'csv':
        write_csv(data, output_file=output)
    elif format == 'sql':
        write_sql(data, table_name='test_table', output_file=output)
    else:
        click.echo(f'Format {format} not supported.', err=True)

if __name__ == '__main__':
    generate() 
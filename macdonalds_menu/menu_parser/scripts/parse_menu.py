import click

from macdonalds_menu.menu_parser.core.parse import save_product_to_json


@click.command()
@click.argument('dst_filepath', type=click.Path())
def parse_menu_cli(dst_filepath):
    """Parse and save product data to a JSON file."""
    save_product_to_json(dst_filepath)
    click.echo(f"Product data saved to {dst_filepath}")


if __name__ == '__main__':
    parse_menu_cli()

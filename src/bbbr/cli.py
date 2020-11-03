import os

import click
from flask.cli import AppGroup
from playhouse.dataset import DataSet

from .models import db

data_cli = AppGroup('data', help='Data utilities')


@data_cli.command('dump')
@click.option(
    '-f', '--format', 'data_format', type=click.Choice(['json', 'csv']), default='json',
    show_default=True, help='select data export format, json or csv',
)
@click.argument('directory_name', type=click.Path(file_okay=False, dir_okay=True))
def data_dump(data_format, directory_name):
    db.close()
    ds = DataSet(db)
    for table_name in ds.tables:
        file_name = os.path.abspath(
            os.path.join(directory_name, f'{table_name}.{data_format}')
        )
        table = ds[table_name]
        ds.freeze(table.all(), format=data_format, filename=file_name)


@data_cli.command('load')
@click.option(
    '-f', '--format', 'data_format', type=click.Choice(['json', 'csv']), default='json',
    show_default=True, help='select data import format, json or csv',
)
@click.argument('directory_name', type=click.Path(file_okay=False, dir_okay=True))
def data_load(data_format, directory_name):
    db.close()
    ds = DataSet(db)
    for table_name in ['users', 'revokedtoken', 'brewery', 'beer', 'rating']:
        file_name = os.path.abspath(
            os.path.join(directory_name, f'{table_name}.{data_format}')
        )
        if os.path.isfile(file_name):
            table = ds[table_name]
            table.thaw(format=data_format, filename=file_name, strict=True)

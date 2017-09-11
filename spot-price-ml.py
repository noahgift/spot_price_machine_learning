#!/usr/bin/env python
"""Pricing Utility"""


import click
import pandas as pd
from sensible.loginit import logger

from paws.spot_pricing_ml import (setup_spot_data, 
        get_spot_pricing_history, combined_spot_df, 
        cluster, recommend_cluster)

log = logger(__name__)

@click.group()
def cli():
    """Spot Pricing Machine Learning Tool"""

@cli.command("history")
@click.option('--instance', help='Instance Type')
def history(instance):
    """Creates Descriptive Statistics of the history of pricing for an instance

    Example usage:

    ./spot-price-ml.py history --instance c3.8xlarge

    """
    pricing_df = setup_spot_data("data/ec2-prices.csv")
    names = pricing_df["InstanceType"].to_dict()
    spot_history_df = get_spot_pricing_history(names, 
        product_description="Linux/UNIX")
    df = combined_spot_df(spot_history_df, pricing_df)
    vals = df.loc[df['InstanceType'] == instance]
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    click.echo(vals.describe())

@cli.command("describe")
@click.option('--sort', default="price_ecu_spot", help='Instance Type')
def describe(sort):
    """Creates clustered description of spot prices, output as median value

    Example usage:

    ./spot-price-ml.py describe

    """
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    pricing_df = setup_spot_data("data/ec2-prices.csv")
    names = pricing_df["InstanceType"].to_dict()
    spot_history_df = get_spot_pricing_history(names, 
        product_description="Linux/UNIX")
    df = combined_spot_df(spot_history_df, pricing_df)
    df_cluster = cluster(df, sort_by=sort)
    click.echo(df_cluster[["SpotPrice", "price_ecu_spot", "cluster", "price_memory_spot"]])

@cli.command("recommend")
@click.option('--instance', help='Instance Type')
def recommend(instance):
    """Recommends similar spot instances uses kNN clustering

    Example usage:

    ./spot-price-ml.py recommend --instance c3.8xlarge 

    """
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    pricing_df = setup_spot_data("data/ec2-prices.csv")
    names = pricing_df["InstanceType"].to_dict()
    spot_history_df = get_spot_pricing_history(names, 
        product_description="Linux/UNIX")
    df = combined_spot_df(spot_history_df, pricing_df)
    df_cluster = cluster(df, sort_by="price_ecu_spot")
    df_cluster_members = recommend_cluster(df_cluster, instance)
    click.echo(df_cluster_members[["SpotPrice", "price_ecu_spot", "cluster", "price_memory_spot"]])

if __name__ == '__main__':
    cli()
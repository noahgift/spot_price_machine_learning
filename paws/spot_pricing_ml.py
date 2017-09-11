"""Spot Pricing Machine Learning"""

from sensible.loginit import logger

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import boto3

log = logger(__name__)

def setup_spot_data(spot_instance_csv="../data/ec2-prices.csv"):
    """Returns a DataFrame of information about spot instances"""

    pricing_df = pd.read_csv(spot_instance_csv)
    pricing_df['price_per_ecu_on_demand'] =\
         pricing_df['linux_on_demand_cost_hourly']/pricing_df['compute_units_ecu']
    return pricing_df

def get_spot_pricing_history(names, product_description="Linux/UNIX", region_name='us-west-2'):
    """Requires a list of instance types 'names' to look up price history for"""

    client = boto3.client('ec2', region_name=region_name)
    response =client.describe_spot_price_history(InstanceTypes = list(names.values()),
        ProductDescriptions = [product_description])
    spot_price_history = response['SpotPriceHistory']
    spot_history_df = pd.DataFrame(spot_price_history)
    spot_history_df.SpotPrice = spot_history_df.SpotPrice.astype(float)
    return spot_history_df

def combined_spot_df(spot_history_df, pricing_df):
    """Combines spot history and pricing df"""

    df = spot_history_df.merge(pricing_df, how="inner", on="InstanceType")
    df['price_memory_spot'] = df['SpotPrice']/df['memory_gb']
    df['price_ecu_spot'] = df['SpotPrice']/df['compute_units_ecu']
    return df

def cluster(combined_spot_history_df, sort_by="price_ecu_spot"):
    """Clusters Spot Instances"""

    df_median = combined_spot_history_df.groupby("InstanceType").median()
    df_median["InstanceType"] = df_median.index
    df_median["price_ecu_spot"] = df_median.price_ecu_spot.round(3)
    df_median.sort_values(sort_by, inplace=True)
    numerical_df = df_median.loc[:,["price_ecu_spot", "price_memory_spot", "SpotPrice"]]
    scaler = MinMaxScaler()
    scaler.fit(numerical_df)
    scaler.transform(numerical_df)
    k_means = KMeans(n_clusters=3)
    kmeans = k_means.fit(scaler.transform(numerical_df))
    df_median["cluster"]=kmeans.labels_
    return df_median

def recommend_cluster(df_cluster, instance_type):
    """Takes a instance_type and finds a recommendation of other instances similar"""


    vals = df_cluster.loc[df_cluster['InstanceType'] == instance_type]
    cluster_res = vals['cluster'].to_dict()
    cluster_num = cluster_res[instance_type]
    cluster_members = df_cluster.loc[df_cluster["cluster"] == cluster_num]
    return cluster_members
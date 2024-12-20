"""
Methods for reading vehiclelivedata from json
"""

import pandas as pd
import json

from ..vehicleInformation import encode_line_name

vehicledata_columns = ["lineid", "category", "direction", "status", "latitude", "longitude", "bearing", "type"]
vehicledata_index_names = ['time', 'vehicleid']

def verify_vehicledata_format(dataframe: pd.DataFrame) -> bool:
    """
    checks if dataframe contains a valid vehicle data format
    Args:
        dataframe: dataframe to check

    Throws: Value error if dataframe is not formatted correctly

    """

    expected_columns = set(vehicledata_columns)
    if not expected_columns.difference(set(dataframe.columns)) == {}: # TODO maybe geht das auch klarer??
        ValueError("dataframe columns do not match expected columns")

    expected_index_names = set(vehicledata_index_names)
    if not expected_index_names.difference(set(dataframe.index.names)) == {}:
        ValueError("dataframe index names do not match expected names")

    return True

## data reading
def vehicledata_from_json(vehicledata_json_dict: dict)-> pd.DataFrame:
    """ extracts service information of public transport vehicles into a Dataframe

    Args:
        vehicledata_json_dict (JSON dict): data structured like vehicleData from HEAG vehicleLivedata api

    Returns:
        DataFrame: contains the information from the vehicleData, indexed with timestamp and vehicleId
    """

    # TODO check whether json has correct format
    # TODO error handling?

    vehicledata_df = pd.DataFrame.from_dict(vehicledata_json_dict['vehicles'])
    # found no use for this data ->  TODO: maybe use reindex instead??
    vehicledata_df = vehicledata_df.drop(columns=['deviation','offline','delay','fillLevels','encodedPath'])

    # lowercase colums work better with database
    vehicledata_df.columns = vehicledata_df.columns.str.lower()

    # use timestamp vehicleId multiindex -> TODO überlege ob das sinvoll ist (bei db sollte alles in colums stehen, sonnst ist vllt anders praktisch), ist jetzt aba alles darauf ausgelegt
    vehicledata_df.index = pd.MultiIndex.from_product(
                                            [[pd.Timestamp(vehicledata_json_dict['timestamp'])],
                                                    vehicledata_df['vehicleid']],
                                                    names= vehicledata_index_names )

    vehicledata_df['lineid'] = vehicledata_df['lineid'].map(encode_line_name)

    # make sure columns are the expected ones
    vehicledata_df = vehicledata_df.reindex(columns = vehicledata_columns)

    return vehicledata_df

def vehicledata_from_json_files(vehicledata_json_file_paths: list)-> pd.DataFrame:
    """ reads vehicleData from .json files and
    extracts service information of public transport vehicles into a Dataframe

    Args:
        vehicledata_json_file_paths (list): list of paths pointing to the .json files containing the vehicleData

    Returns:
        DataFrame: contains the information from the vehicleData, indexed with timestamp and vehicleId
    """

    vehicledata_df_list = []
    for file_path in vehicledata_json_file_paths:
        with open(file_path) as json_file:
            vehicledata_df_list.append(vehicledata_from_json(json.load(json_file)))
    return pd.concat(vehicledata_df_list)


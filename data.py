import requests
import pandas as pd
import keys


# API URL's
URL_REBRICK = "https://rebrickable.com"
URL_BRICKSET = "https://brickset.com/api/v3.asmx"


def get_mocs(code, parts, params):
    """Writes a file containing the info of the MOCs of a specific Lego set.
    Returns a tuple containing the number of MOCs of a Lego set and the average number of parts in
    these MOCs.
    """

    response = requests.get(f"{URL_REBRICK}/api/v3/lego/sets/{code}/alternates", params=params)
    data = response.json()

    # Check that JSON file contains data. If not, return from function.
    if data["count"] == 0:
        return (0, 0)

    moc_list= []

    for n in range(len(data["results"])):
        moc_dict = {
            "set_num": data['results'][n]['set_num'],
            "name": data['results'][n]['name'],
            "num_parts": data['results'][n]['num_parts'],
            "moc_url": data['results'][n]['moc_url']
        }
        moc_list.append(moc_dict)

    mocs_df = pd.DataFrame(moc_list)

    # Remove "-1" from the end of the set number
    code = code.split("-")[0]
    # Sort dataframe based on the number of parts in a MOC
    mocs_df = mocs_df.sort_values("num_parts", ascending=False)

    # mocs_df['name'] = mocs_df['name'].str.replace(code, '', regex=True)

    # Count the percentage of pieces used in relation to the original set. Remove MOC's using extra pieces.
    mocs_df["pieces_used_percentage"] = round((mocs_df["num_parts"] / parts) * 100, 1)
    mocs_df = mocs_df.query("pieces_used_percentage < 100")

    # Create .csv file
    mocs_df.to_csv(f"{code}-MOCs.csv")

    return (len(mocs_df), (mocs_df["num_parts"].mean()))

def get_lego_info():
    """Writes a csv file listing the information of all the Lego sets given in 'my_lego_sets.csv'.
    Also creates separate files for every set containing a list of the MOCs for that set.
    Returns a DataFrame containing data of all Lego sets.
    """

    # Read a file containing Lego set numbers and convert the content to a list.
    try:
        my_own_legos = pd.read_csv("my_lego_sets.csv")
    except:
        print("No file found")
    else:
        own_legos_list = my_own_legos["Set number"].to_list()

        # Parameters for the Rebrick API call.
        params_rb = {
            "key": keys.APIKEY_REBRICK
        }

        # Create a list for the creation of a pandas DataFrame
        lego_list = []

        # For every set number get all necessary info using Rebrick and Brickset APIs.
        for code in own_legos_list:
            rebrick_code = str(code) + "-1"

            response_rb = requests.get(f"{URL_REBRICK}/api/v3/lego/sets/{rebrick_code}", params=params_rb)

            data_rb = response_rb.json()

            # Check that JSON file contains data. If not, continue to the next set number.
            try:
                data_point = data_rb["num_parts"]
            except (KeyError, IndexError, TypeError):
                continue

            # Get all MOCs of the set and write them in a csv file.
            num_mocs, avg_moc_parts = get_mocs(rebrick_code, data_rb["num_parts"], params_rb)

            # Parameters for Brickset API call.
            params_bs = {
                "apiKey": keys.APIKEY_BRICKSET,
                "setNumber": code
            }

            response_bs = requests.get(f"{URL_BRICKSET}/getInstructions2", params=params_bs)
            data_bs = response_bs.json()

            # A dictionary for storing the data of one Lego set
            lego_dict = {}

            # Add data to dictionary
            lego_dict = {
                "set_num": str(code),
                "name": data_rb["name"],
                "num_parts": data_rb["num_parts"],
                "num_mocs": num_mocs,
                "avg_moc_parts": avg_moc_parts,
                "instruction_url": data_bs["instructions"][0]["URL"]
            }

            # Add dictionary to list of Lego set data
            lego_list.append(lego_dict)

        # Create a Pandas Dataframe from the list, sort it by set number and write to a csv file
        legos_df = pd.DataFrame(lego_list)
        legos_df = legos_df.sort_values("set_num")
        legos_df.to_csv("lego_info.csv")

        return legos_df


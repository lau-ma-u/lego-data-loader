
import requests
import pandas as pd

APIKEY_REBRICK = "3337cebab7512a581f12cccf7fafb08c"
URL_REBRICK = "https://rebrickable.com"

APIKEY_BRICKSET = "3-z8CQ-fpEO-nvPx2"
URL_BRICKSET = "https://brickset.com/api/v3.asmx"

def get_mocs(code, parts, params):
    response = requests.get(f"{URL_REBRICK}/api/v3/lego/sets/{code}/alternates", params=params)
    data = response.json()

    moc_set_nums = []
    moc_names = []
    moc_num_parts = []
    moc_urls = []

    for n in range(len(data["results"])):
        moc_set_nums.append(data['results'][n]['set_num'])
        moc_names.append(data['results'][n]['name'])
        moc_num_parts.append(data['results'][n]['num_parts'])
        moc_urls.append(data['results'][n]['moc_url'])

    moc_dict = {
        "set_num": moc_set_nums,
        "name": moc_names,
        "num_parts": moc_num_parts,
        "instruction_url": moc_urls
    }

    mocs_df = pd.DataFrame(moc_dict)
    mocs_df = mocs_df.sort_values("num_parts", ascending=False)
    mocs_df["pieces_used_percentage"] = round((mocs_df["num_parts"] / parts) * 100, 1)
    mocs_df = mocs_df.query("pieces_used_percentage < 100")

    code = code.split("-")[0]
    mocs_df.to_csv(f"{code}-MOCs.csv")


my_own_legos = pd.read_csv("my_lego_sets.csv")

own_legos_list = my_own_legos["Set number"].to_list()

params_rb = {
    "key": APIKEY_REBRICK
}

set_numbers = []
names = []
parts = []
instructions = []

for code in own_legos_list:
    rebrick_code = str(code) + "-1"
    response_rb = requests.get(f"{URL_REBRICK}/api/v3/lego/sets/{rebrick_code}", params=params_rb)
    data_rb = response_rb.json()

    get_mocs(rebrick_code, data_rb["num_parts"], params_rb)

    params_bs = {
        "apiKey": APIKEY_BRICKSET,
        "setNumber": code
    }

    response_bs = requests.get(f"{URL_BRICKSET}/getInstructions2", params=params_bs)
    data_bs = response_bs.json()

    set_numbers.append(str(code))
    names.append(data_rb["name"])
    parts.append(data_rb["num_parts"])
    instructions.append(data_bs["instructions"][0]["URL"])

lego_dict = {
    "set_num": set_numbers,
    "name": names,
    "num_parts": parts,
    "instruction_url": instructions
}

legos_df = pd.DataFrame(lego_dict)
legos_df = legos_df.sort_values("set_num")
legos_df.to_csv("lego_info.csv")



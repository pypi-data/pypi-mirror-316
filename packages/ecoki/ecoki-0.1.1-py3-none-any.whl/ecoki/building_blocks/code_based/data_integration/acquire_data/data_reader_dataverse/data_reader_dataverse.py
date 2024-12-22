from pyDataverse.api import NativeApi, DataAccessApi
from pyDataverse.models import Dataverse
from pyDataverse.utils import read_file

from ecoki.building_block_framework.building_block import BuildingBlock

import pandas as pd
from io import BytesIO


class DataReaderDataverse(BuildingBlock):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.architecture = "EcoKI"
        self.description = "Read data from ecoKI dataverse repository"
        self.version = "1"
        self.category = ""

        self.add_outlet_port('output_data', pd.DataFrame)

        self.loading_icon = None

        self.data = None

    def download_from_dataverse(self, BASE_URL, API_TOKEN, param):
        data_api = DataAccessApi(BASE_URL, API_TOKEN)

        if self.interactive_settings:
            data_file_id = param
        else:  # {"base_url", "token", "doi", "name"}
            api = NativeApi(BASE_URL, API_TOKEN)
            DOI = param
            dataset = api.get_dataset(DOI)
            data_files_list = dataset.json()['data']['latestVersion']['files']

            data_files_dict = {}
            for datafile in data_files_list:
                filename = datafile["dataFile"]["filename"]
                file_id = datafile["dataFile"]["id"]
                data_files_dict[filename] = file_id
            data_file_id = data_files_dict[self.settings["name"]]

        response = data_api.get_datafile(data_file_id)
        if self.loading_icon:
            self.loading_icon.value = False

        data = BytesIO(response.content)
        self.data = pd.read_csv(data)

    def execute(self):
        BASE_URL = self.settings["base_url"]
        API_TOKEN = self.settings["token"]

        if self.interactive_settings:
            pass
        else:
            param = self.settings["doi"]

            self.download_from_dataverse(BASE_URL, API_TOKEN, param)

        if self.settings["index_name"]:
            if self.settings["index_name"].isdigit():
                self.settings["index_name"] = int(self.settings["index_name"])
            self.data.set_index(self.settings["index_name"], inplace=True)

        return {"output_data": self.data}

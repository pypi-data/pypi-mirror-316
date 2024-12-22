import numpy as np
import json
from .data_types import get_data_type_info
import struct
import pandas as pd


class JSONStructureError(Exception):
    pass


class TauLogDecoder:
    def __init__(self):
        self._messages: list = []
        self._data_pd: dict[pd.DataFrame] = {}

    @property
    def data(self):
        return self._data_pd

    def load_structure_from_json(self, filepath: str) -> None:
        self._messages.clear()
        self._data_pd.clear()

        with open(filepath, "r") as f:
            raw_structure = json.load(f)

        for msg_name in raw_structure.keys():
            msg_length = 1
            msg_decode_string = ""
            msg = raw_structure[msg_name]

            if len(msg["data_field_names"]) != len(msg["data_field_types"]):
                raise JSONStructureError(
                    f"Different length of name and data type arrays in message: {msg_name}"
                )

            data_type_dict = dict()
            for i in range(len(msg["data_field_names"])):
                data_type = msg["data_field_types"][i]
                data_type_info = get_data_type_info(data_type)
                msg_length += data_type_info["length"]
                msg_decode_string += data_type_info["decode_symbol"]
                data_type_dict[msg["data_field_names"][i]] = data_type_info[
                    "python_type"
                ]

            msg_info = {
                "name": msg_name,
                "index": msg["index"],
                "length": msg_length,
                "decode_string": msg_decode_string,
                "data_field_names": msg["data_field_names"],
                "python_data_types": data_type_dict,
            }
            self._messages.append(msg_info)
            self._data_pd[msg_name] = pd.DataFrame(
                data={}, columns=msg["data_field_names"]
            )

    def decode_log(self, filepath: str) -> None:
        with open(filepath, "rb") as f:
            log_raw = f.read()

        log_decoding_completed = False
        while not log_decoding_completed:
            if len(log_raw) == 0:
                log_decoding_completed = True
            else:
                msg_key = log_raw[0]
                for i in range(len(self._messages)):
                    if self._messages[i]["index"] == msg_key:
                        msg_name = self._messages[i]["name"]
                        msg_fields = self._messages[i]["data_field_names"]
                        msg_length = self._messages[i]["length"]
                        msg_decode_string = self._messages[i]["decode_string"]

                        if len(log_raw) < msg_length:
                            log_decoding_completed = True
                            break

                        msg_data = struct.unpack(
                            msg_decode_string, log_raw[1:msg_length]
                        )
                        self._data_pd[msg_name].loc[
                            len(self._data_pd[msg_name])
                        ] = msg_data
                        log_raw = log_raw[msg_length:]
                        break
        for i in range(len(self._messages)):
            msg_name = self._messages[i]["name"]
            convert_dict = self._messages[i]["python_data_types"]
            self._data_pd[msg_name] = self._data_pd[msg_name].astype(convert_dict)

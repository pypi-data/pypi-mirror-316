import unittest
import sys
import os

from src.tau_log.log_decoder import TauLogDecoder


class TestLogDecoder(unittest.TestCase):
    def test_all(self):
        log_decoder = TauLogDecoder()
        log_decoder.load_structure_from_json("./structure_1.json")
        log_decoder.decode_log("./log_1.tau")
        data = log_decoder.data

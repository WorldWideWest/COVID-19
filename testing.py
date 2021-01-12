import os
import unittest
import pandas as pd
import numpy as np


class Testing(unittest.TestCase):

    def testing_dataFrame_shape(self):
        """Testing the DataFrame shape"""
    
        path = "./dataSet/rawData"
        fileName = ["mbih.xlsx", "bih.xlsx", "fbih.xlsx", "rs.xlsx"]
        
        for name in fileName:
            if name == "mbih.xlsx":
                data = pd.read_excel(os.path.join(path, name), engine = "openpyxl")
                self.assertEqual(data.shape[1], 4)
            else:
                data = pd.read_excel(os.path.join(path, name), engine = "openpyxl")
                self.assertEqual(data.shape[1], 7)

    def testing_clean_dataFrame(self):
        """Testing for missing Values in the clean dataFrame's"""

        fileName = ["cleanData.xlsx", "bd.xlsx", "fbih.xlsx", "rs.xlsx"]        
        path = "./dataSet/cleanData"

        for name in fileName:
            if name == "cleanData.xlsx":
                data = pd.read_excel(os.path.join(path, name), engine = "openpyxl")
                self.assertEqual(data.shape[1], 7)
                for number in data.isnull().sum():
                    self.assertEqual(number, 0)
            else:
                data = pd.read_excel(os.path.join(path, name), engine = "openpyxl")
                self.assertEqual(data.shape[1], 5)
                for number in data.isnull().sum():
                    self.assertEqual(number, 0)

if __name__ == '__main__':
    unittest.main()

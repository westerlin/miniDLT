# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 11:36:18 2018

@author: raw
"""

import importlib

module = importlib.import_module("smartcontract")
SmartContract = getattr(module,"SmartContract")
contract = SmartContract()
#self.__log__(contract.execute())
print(contract.execute())
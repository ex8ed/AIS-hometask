# -*- coding: UTF-8 -*-
"""Contains core functions to make simulators structure and to write it to a file"""
from json import dumps


class Simulator:
    """Class contains objects for every sim parameter."""
    def __init__(self, name_, type_):
        """
        Base sim constructor; provides structures to contain data.
        :param type_: simulator type (booksim, dec9 ...)
        :param name_: simulator name in UHLNoCS
        """
        self.__parameters = dict()
        self.__model_type = type_
        self.__model_name = name_

    def reset_parameters(self):
        """
        Clears params.
        :return: clean dict
        """
        self.__parameters.clear()

    def set_parameter(self, key, val):
        """
        Setting new pairs of parameters in dict.
        :param key: key for sim parameter JSON
        :param val: value
        """
        self.__parameters.setdefault(key, val)

    def set_name(self, n_name):
        """
        Sets new name for simulator
        :param n_name: new name for UHLNoCS
        """
        self.__model_name = n_name

    def set_type(self, n_type):
        """
        Sets new type for simulator
        :param n_type: new type
        :return:
        """
        self.__model_type = n_type

    def type(self):
        """
        Type getter
        :return: type of simulator
        """
        return self.__model_type

    def name(self):
        """
        Name getter
        :return: name of simulator
        """
        return self.__model_name

    def params(self):
        """
        Parameters getter
        :return: parameters of simulation
        """
        return self.__parameters

    def export(self):
        """
        Adds necessary fields for JSON structure.
        :return: dict with necessary fields.
        """
        return {f'{self.__sim_types[self.__model_type]}NocParameters': self.__parameters,
                'modelType': self.__model_type,
                'nameModel': self.__model_name}

    # private dict which helps convert fields for extractor
    __sim_types = {0: 'uocns',
                   1: 'booksim',
                   2: 'newxim',
                   3: 'topaz',
                   4: 'dec9',
                   5: 'gpNocSim'}


class Extractor:
    """Tool which allows convert objects to JSON and write it to a file"""
    def __init__(self, file_name, dir_='./'):
        """
        Base constructor; there is name of file and directory to be written.
        Default dir: current catalog
        :param file_name: name of file
        :param dir_: directory to be written. DEFAULT: "./"
        """
        self.__name = file_name
        self.__directory = dir_

    @classmethod
    def to_json(cls, obj):
        """
        Allows convert python-objects to a JSON format;
        Can be used without instances.
        :param obj: any python-object
        :return: JSON formatted given object
        """
        return dumps(obj, indent=2)

    def writer(self, obj):
        """
        Write info to a JSON file, using information from self fields
        :param obj: JSON object
        """
        with open(f"{self.__directory}{self.__name}.json", 'a+') as file:
            file.writelines(obj)

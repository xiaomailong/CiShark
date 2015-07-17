# -*- coding: utf-8 -*-
__author__ = 'Administrator'

from .ModelBase import ModelBase

class DataDict(ModelBase):
    """

    """

    query = (" SELECT enum_name,fd_value"
             " FROM data_dict"
             " WHERE tb_name = 'log' AND fd_name = 'log_type'")
    ModelBase.cursor.execute(query)
    values = ModelBase.cursor.fetchall()

    log_type_dict = dict(values)

    # print(log_type_dict)

    def __init__(self):
        super().__init__()

        pass

    @staticmethod
    def get_log_type_id(log_type_str):
        """

        :return:
        """

        return DataDict.log_type_dict.get(log_type_str,0)

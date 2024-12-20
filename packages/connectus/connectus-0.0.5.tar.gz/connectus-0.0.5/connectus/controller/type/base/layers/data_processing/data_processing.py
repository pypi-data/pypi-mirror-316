from connectus.tools.structure.data import DataResponse, VariableData, DataRequest
from abc import ABC, abstractmethod

class BaseDataProcessing(ABC):
    def __init__(self):
        pass
    
    def process(self, request_list: list[DataRequest]) -> list[dict[str, any]]: # we have output_data ??
        try:
            output_data = []
            if request_list:
                for request in request_list:
                    request_dict = request.nested_model()
                    if 'update_data' == request_dict['action']:
                        self._process_data(request_dict['data'])
                    elif 'error' == request_dict['action']:
                        pass
                    else:
                        raise ValueError('Data type not recognized during processing data')
            return output_data
        except Exception as e:
            print('An error occurred during processing data: ', e)

    def _process_data(self, variable_list: list[VariableData]):
        ''' Update the device data with the new values and save them in the database'''
        try:
            if variable_list:
                for variable in variable_list:
                    self.controller.data.update(variable)
        except Exception as e:
            print('An error occurred while processing the data update: ', e)
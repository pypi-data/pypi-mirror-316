from connectus.tools.structure.data import DataRequest
from abc import ABC, abstractmethod

class BaseDispatch(ABC):
    def __init__(self):
        pass
    
    def send_command(self, request_list: list[DataRequest], node_params: dict[str, any]):
        if request_list:
            for request in request_list:
                self.device.node.write(request, node_params)
from connectus.tools.structure.data import DataRequest
from connectus.data_manager.node.type.base import BaseNode
from .configuration import Configuration
from .configuration.tools.subscription import SubscriptionHandler
from asyncua import ua
import asyncio

class OPC(BaseNode, Configuration):
    def __init__(self, node_config: dict[str, str], stop_event: asyncio.Event):
        BaseNode.__init__(self, stop_event)
        Configuration.__init__(self, node_config)
    
    async def connect(self):
        try:
            await self.create_client()
            await self.set_data_location()
            self.subscription = await self.create_subscription(1000)
        except Exception as e:
            raise ConnectionError(f"An error occurred while connecting to the OPC server: {e}")
        
    async def disconnect(self):
        try:
            if await self.client.check_connection():
                await self.client.disconnect()
        except Exception as e:
            print(f"An error occurred while disconnecting from the OPC server: {e}")

    async def create_subscription(self, period: int):
        try:
            handler = SubscriptionHandler(self.buffer)
            self.subscription = await self.client.create_subscription(period, handler)
            nodes = []
            for _, data in self.devices.items():
                for variable in data['folder']['variables']:
                    nodes.append(variable['instance'])
            await self.subscription.subscribe_data_change(nodes)
        except Exception as e:
            print(f"An error occurred while creating the subscription: {e}")

    def read(self):
        try:
            pass
        except Exception as e:
            print(f"An error occurred while reading the data: {e}")

    def write(self, request_list: list[DataRequest], node_params: dict[str, any]): ## include check if variable exists in the server/device
        try:
            if request_list:
                for request in request_list:
                    data_dict = request.nested_model()['data'].plain_model()
                    print(data_dict)


            # for item in data_dict:
            #     for variable_name, variable_value in item.items():
            #         for device in self.devices:
            #             for variable in self.devices[device]['folder']['variables']:
            #                 if variable['name'] == variable_name:
            #                     variable['instance'].write_value(variable_value)
        except Exception as e:
            print(f"An error occurred while writing the data: {e}")


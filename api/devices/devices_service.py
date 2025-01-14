from api.devices.devices_action import DevicesDAO

class DevicesService:
    def __init__(self, dao: DevicesDAO):
        self.dao = dao

    def get_devices(self, data):
        return self.dao.get_devices(data)

    def get_device(self, device_id):
        return self.dao.get_device(device_id)

    def delete_device(self, device_id):
        return self.dao.delete_device(device_id)

    def add_device(self, data):
        return self.dao.add_device(data)

    def edit_device(self, data, device_id):
        return self.dao.edit_device(data, device_id)

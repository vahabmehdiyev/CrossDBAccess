from flask_restx import Resource, Namespace
from config.implemented import devices_service
from api.utils.utils import csrf_protected
from flask import request

devices_ns = Namespace('api/devices')

@devices_ns.route('/')
class DevicesView(Resource):
    @csrf_protected
    def get(self):
        data = request.args
        return devices_service.get_devices(data)

@devices_ns.route('/<device_id>/')
class DeviceView(Resource):
    @csrf_protected
    def get(self, device_id):
        return devices_service.get_device(device_id)

@devices_ns.route('/add/')
class AddDeviceView(Resource):
    @csrf_protected
    def post(self):
        data = request.get_json()
        return devices_service.add_device(data)

@devices_ns.route('/delete/<device_id>/')
class DeleteDeviceView(Resource):
    @csrf_protected
    def delete(self, device_id):
        return devices_service.delete_device(device_id)

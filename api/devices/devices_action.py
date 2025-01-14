from api.devices.devices_model import Device, Item, Category, CategoryType, DeviceRemote
from flask import request, g
from sqlalchemy import String, cast, func
from api.utils.utils import jwt_required, pagination, ordering
from config.database import get_remote_session

class DevicesDAO:
    def __init__(self, session):
        self.session = session

    @jwt_required
    def get_devices(self, data):
        lang = request.headers.get('Accept-Language', 'en')

        # Local devices
        devices_local = self.session.query(Device).order_by(Device.id.desc()).all()
        for device in devices_local:
            setattr(device, 'is_external', False)

        # Remote devices
        remote_session = get_remote_session()
        try:
            devices_remote = remote_session.query(DeviceRemote).order_by(DeviceRemote.id.desc()).all()
            for device in devices_remote:
                setattr(device, 'is_external', True)
        finally:
            remote_session.close()

        devices = devices_local + devices_remote

        # Filter and search
        if data.get('filter') and data.get('search'):
            search = f"%{data.get('search').lower()}%"
            if data.get('filter') == 'serial_number':
                devices_local = self.session.query(Device).filter(Device.serial_number.like(search)).all()
                remote_session = get_remote_session()
                try:
                    devices_remote = remote_session.query(DeviceRemote).filter(DeviceRemote.serial_number.like(search)).all()
                finally:
                    remote_session.close()
                devices = devices_local + devices_remote

            elif data.get('filter') == 'item':
                item_ids = [device.item for device in devices]
                remote_session = get_remote_session()
                matching_items = remote_session.query(Item.id).filter(
                    Item.id.in_(item_ids),
                    func.lower(Item.name).like(search)
                ).all()
                matching_item_ids = [item.id for item in matching_items]
                devices = [device for device in devices if device.item in matching_item_ids]
                remote_session.close()

        results = []
        remote_session = get_remote_session()
        try:
            for device in devices:
                item = remote_session.query(Item).filter_by(id=device.item).first()
                category = remote_session.query(Category).filter_by(id=device.category).first()
                category_type = remote_session.query(CategoryType).filter_by(id=device.category_type).first()

                device_data = {
                    'id': device.id,
                    'item': item.name if item else "Unknown",
                    'serial_number': device.serial_number,
                    'category': f'{category.name}' if category else None,
                    'category_type': category_type.name if category_type else None,
                    'is_external': getattr(device, 'is_external', None),
                }
                results.append(device_data)
        finally:
            remote_session.close()

        keys = list(results[0].keys()) if results else []
        if data.get('ordering'):
            results = ordering(data, keys, results)

        response = pagination(data, results)
        return response

    @jwt_required
    def get_device(self, device_id):
        lang = request.headers.get('Accept-Language', 'en')
        device = self.session.query(Device).filter(Device.id == device_id).first()

        if not device:
            remote_session = get_remote_session()
            device = remote_session.query(DeviceRemote).filter(DeviceRemote.id == device_id).first()
            remote_session.close()

        if not device:
            return {"message": "Device not found"}, 404

        remote_session = get_remote_session()
        item = remote_session.query(Item).filter_by(id=device.item).first()
        category_type = remote_session.query(CategoryType).filter_by(id=device.category_type).first()
        category = remote_session.query(Category).filter_by(id=device.category).first()

        result = {
            'id': device.id,
            'serial_number': device.serial_number,
            'item': item.id if item else None,
            'category_type': category_type.name if category_type else None
        }

        if category_type and category_type.name == 'electronics' and category:
            result['category_id'] = category.id

        remote_session.close()
        return result, 200

    @jwt_required
    def delete_device(self, device_id):
        device = self.session.query(Device).filter(Device.id == device_id).first()
        if not device:
            return {"message": "Device not found"}, 404

        self.session.delete(device)
        self.session.commit()
        return {"message": "Device deleted successfully"}, 200

    @jwt_required
    def add_device(self, data):
        try:
            serial_number = data.get('serial_number')
            item = data.get('item_id')
            category_type = data.get('category_type')
            user_id = g.user_id

            new_device = Device(
                serial_number=serial_number,
                item=item,
                category_type=category_type,
                user_id=user_id
            )
            self.session.add(new_device)
            self.session.commit()
            return {"message": "Device added successfully"}, 200

        except Exception as e:
            return {"error": str(e)}, 500

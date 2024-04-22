from __init__ import db

all_roomTypes = [
    {'filename': 'deluxe.jpg', 'filename_layout': 'deluxe_super.jpg', 'name': 'deluxe', 'price': 19.99, 'area': 6,
     'unit': 'sq m', 'length': 2.1, 'width': 2.6},
    {'filename': 'single.jpg', 'filename_layout': 'single_single.jpg', 'name': 'standard', 'price': 16.99, 'area': 5,
     'unit': 'sq m', 'length': 2.1, 'width': 2.2}
]


class RoomType(db.Document):
    meta = {'collection': 'rooms'}
    filename = db.StringField()
    filename_layout = db.StringField()
    name = db.StringField()
    price = db.FloatField()
    area = db.IntField()
    unit = db.StringField()
    length = db.FloatField()
    width = db.FloatField()

    @staticmethod
    def getAllRoomTypes():
        roomTypes = RoomType.objects()
        if not roomTypes:
            for r in all_roomTypes:
                RoomType(**r).save()

            roomTypes = RoomType.objects()

        return roomTypes

    @staticmethod
    def getRoomType(name):
        return RoomType.objects(name=name).first()

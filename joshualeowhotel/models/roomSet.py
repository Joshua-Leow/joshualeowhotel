from __init__ import db
from models.amenities import AmenityType
from models.beds import BedType
from models.rooms import RoomType


class roomSet(db.Document):
    meta = {'collection': 'roomSet'}
    RoomType = db.ReferenceField(RoomType)
    BedType = db.ReferenceField(BedType)
    amenities = db.ListField(db.ReferenceField(AmenityType))
    price = db.FloatField()

    @staticmethod
    def createRoom(roomTypeName, bedTypeName, amenityItemCodesList):
        Room_Type = RoomType.getRoomType(roomTypeName)
        Bed_Type = BedType.getBedType(bedTypeName)
        price = Room_Type.price + Bed_Type.price

        amenities = AmenityType.getAllAmenitiesByItemCodesList(amenityItemCodesList)
        for a in amenities:
            price += a.price

        room_Set = roomSet(RoomType=Room_Type, BedType=Bed_Type, amenities=amenities, price=price).save()
        return room_Set

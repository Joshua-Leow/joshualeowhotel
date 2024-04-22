from __init__ import db

all_bedTypes = [
    {'filename': 'super_single_bed.jpg', 'name': 'super single', 'description': 'with one pillow and one blanket',
     'price': 12.99},
    {'filename': 'single_bed.jpg', 'name': 'single', 'description': 'with one pillow and one blanket', 'price': 10.99}
]


class BedType(db.Document):
    meta = {'collection': 'beds'}
    filename = db.StringField()
    name = db.StringField()
    description = db.StringField()
    price = db.FloatField()

    @staticmethod
    def getAllBedTypes():
        bedTypes = BedType.objects()
        if not bedTypes:
            for b in all_bedTypes:
                BedType(**b).save()

            bedTypes = BedType.objects()

        return bedTypes

    @staticmethod
    def getBedType(name):
        return BedType.objects(name=name).first()

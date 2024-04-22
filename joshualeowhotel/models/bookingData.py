from __init__ import db
from models.roomSet import roomSet
from models.users import User
from datetime import timedelta, datetime


class Booking(db.Document):
    meta = {'collection': 'bookings'}
    id_counter = 0
    booking_id = db.IntField()  # unique booking identifier
    checkInDate = db.DateTimeField()
    checkOutDate = db.DateTimeField()
    roomSet = db.ReferenceField(roomSet)
    user = db.ReferenceField(User)
    status = db.StringField()

    @staticmethod
    def createBooking(checkInDate, checkOutDate, roomSet, user):
        Booking.id_counter += 1  # add 1 to the ID for every booking made
        b = Booking(booking_id=Booking.id_counter, checkInDate=checkInDate, checkOutDate=checkOutDate, roomSet=roomSet,
                    user=user, status="confirmed").save()
        return b

    @staticmethod
    def getBooking(booking_id):
        return Booking.objects(booking_id=booking_id).first()

    @staticmethod
    def getAllBookingsByUser(user):
        return Booking.objects(user=user)

    @staticmethod
    def getNumOfNights(bookingObj):
        return (bookingObj.checkOutDate - bookingObj.checkInDate).days

    @staticmethod
    def getTotalPrice(bookingObj):
        return (bookingObj.getNumOfNights(bookingObj) * bookingObj.roomSet.price)

    # Return True if dates are correct
    @staticmethod
    def validateDates(CheckInDate_obj, CheckOutDate_obj):
        today = datetime.today()
        if CheckInDate_obj > today and CheckInDate_obj < CheckOutDate_obj:
            return True
        else:
            return False

    @staticmethod
    def updateBookingStatus(bookingObj, new_status):
        bookingObj.status = new_status
        bookingObj.save()
        return bookingObj

from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required, current_user

from models.beds import BedType
from models.amenities import AmenityType

from models.rooms import RoomType
from models.bookingData import Booking
from models.roomSet import roomSet
from models.users import User
from models.guest import Guest
from models.forms import GuestForm

import csv, io
import json

from flask import jsonify
from datetime import datetime

booking = Blueprint('booking', __name__)


@booking.route("/book_room", methods=["GET", "POST"])
@login_required
def bookRoom():
    guestForm = GuestForm()
    bookingConfirmation = False
    if request.method == "GET":
        return render_template("book_room.html", \
                               form=guestForm, \
                               RoomTypes=RoomType.getAllRoomTypes(), \
                               BedTypes=BedType.getAllBedTypes(), \
                               Amenities=AmenityType.getAllAmenitiesTypes(), \
                               user=current_user, \
                               bookings=Booking.getAllBookingsByUser(current_user), \
                               bookingConfirmation=bookingConfirmation, \
                               dates_validation=True, \
                               panel="Book Room"
                               )

    else:
        passport = request.form.get("passport")
        country = request.form.get("country")
        roomTypeName = request.form.get("roomTypeName")
        bedTypeName = request.form.get("bedTypeName")
        CheckInDate = request.form.get("CheckInDate")
        CheckInDate_obj = datetime.strptime(CheckInDate, "%Y-%m-%d")
        CheckOutDate = request.form.get("CheckOutDate")
        CheckOutDate_obj = datetime.strptime(CheckOutDate, "%Y-%m-%d")
        amenityItemCodesList = request.form.getlist("amenityItemCodesList[]")

        dates_validation = Booking.validateDates(CheckInDate_obj, CheckOutDate_obj)
        if dates_validation:
            print(f"roomTypeName is {roomTypeName}")
            print(f"bedTypeName is {bedTypeName}")
            print(f"CheckInDate_obj is {CheckInDate_obj}")
            print(f"CheckOutDate_obj is {CheckOutDate_obj}")
            for itemCode in amenityItemCodesList:
                print(f"Selected option: {itemCode}")

            room_Set = roomSet.createRoom(roomTypeName, bedTypeName, amenityItemCodesList)
            roomBookingObj = Booking.createBooking(CheckInDate_obj, CheckOutDate_obj, room_Set, current_user)

            updated_user = User.updateGuest(email=current_user.email,
                                            guestObj=Guest(passport=passport, country=country))
            updated_booking = Booking.updateBookingStatus(bookingObj=roomBookingObj, new_status="confirmed")
            bookingConfirmation = True
            NoOfNights = Booking.getNumOfNights(updated_booking)
            TotalPrice = Booking.getTotalPrice(updated_booking)

            return render_template("book_room.html", \
                                   form=guestForm, \
                                   RoomTypes=RoomType.getAllRoomTypes(), \
                                   BedTypes=BedType.getAllBedTypes(), \
                                   Amenities=AmenityType.getAllAmenitiesTypes(), \
                                   user=updated_user, \
                                   bookings=Booking.getAllBookingsByUser(updated_user), \
                                   roomBookingObj=updated_booking, \
                                   NoOfNights=NoOfNights, \
                                   TotalPrice=TotalPrice, \
                                   bookingConfirmation=bookingConfirmation, \
                                   dates_validation=dates_validation, \
                                   panel="Book Room"
                                   )

        else:
            print('wrong dates')
            return render_template("book_room.html", \
                                   form=guestForm, \
                                   RoomTypes=RoomType.getAllRoomTypes(), \
                                   BedTypes=BedType.getAllBedTypes(), \
                                   Amenities=AmenityType.getAllAmenitiesTypes(), \
                                   user=current_user, \
                                   bookings=Booking.getAllBookingsByUser(current_user), \
                                   bookingConfirmation=bookingConfirmation, \
                                   dates_validation=dates_validation, \
                                   panel="Book Room"
                                   )


@booking.route("/bookings", methods=["GET"])
@login_required
def viewBooking():
    return render_template("bookings.html", \
                           RoomTypes=RoomType.getAllRoomTypes(), \
                           BedTypes=BedType.getAllBedTypes(), \
                           Amenities=AmenityType.getAllAmenitiesTypes(), \
                           user=current_user, \
                           bookings=Booking.getAllBookingsByUser(current_user), \
                           panel="Bookings"
                           )


@booking.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    upload_status = False
    NumOfUploads = 0
    if request.method == 'POST':
        afile = request.files.get('file')
        data = afile.read().decode('utf-8')
        afile.close()

        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        for num, item in enumerate(list(dict_reader)):
            email = item['email']
            name = item['name']
            passport = item['passport']
            country = item['country']
            checkInDate = datetime.strptime(item['checkInDate'], "%d/%m/%Y")
            checkOutDate = datetime.strptime(item['checkOutDate'], "%d/%m/%Y")
            roomTypeName = item['room']
            bedTypeName = item['bed']
            amenityItemCodesList = json.loads(item['amenities'])

            existing_user = User.getUser(email=email)
            if not existing_user:
                existing_user = User.createUser(email=email, name=name, password=None)

            # if not existing_user.guest:
            # Update Guest details even if it is recorded 
            # as they might have changed.
            guestObj = Guest(passport=passport, country=country)
            User.updateGuest(email=email, guestObj=guestObj)
            room_Set = roomSet.createRoom(roomTypeName=roomTypeName, bedTypeName=bedTypeName,
                                          amenityItemCodesList=amenityItemCodesList)
            bookingObj = Booking.createBooking(checkInDate=checkInDate, checkOutDate=checkOutDate, roomSet=room_Set,
                                               user=existing_user)
            NumOfUploads = num + 1
        upload_status = True

    return render_template("upload.html", upload_status=upload_status, NumOfUploads=NumOfUploads, panel="Upload")


@booking.route("/check_in", methods=['GET', 'POST'])
@login_required
def checkIn():
    message = None

    if request.method == 'POST':
        booking_id = request.form.get("booking_id")

        BookingObj = Booking.getBooking(booking_id)
        Booking.updateBookingStatus(BookingObj, 'checkin')

        passport = BookingObj.user.guest.passport
        checkInDate = BookingObj.checkInDate.strftime("%a, %d %b %Y")

        message = f"{passport} checked in on {checkInDate}"

    return render_template("check_in.html", \
                           users=User.getAllUsersWithGuest(), \
                           message=message, \
                           panel="Check In"
                           )


# function called from ajax to get a list of bookings based on user email
# function is called within getBookings() in check_in.html page
@booking.route("/getBookings", methods=['POST'])
@login_required
def getBookings():
    aEmail = request.form.get("aEmail")
    aUser = User.getUser(aEmail)
    bookings = Booking.getAllBookingsByUser(aUser)
    confirmed_bookings = [booking for booking in bookings if booking.status == 'confirmed']
    return jsonify({'data': render_template('check_in_response.html', bookings=confirmed_bookings)})

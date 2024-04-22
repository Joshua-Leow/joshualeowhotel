from flask import Blueprint, request, render_template
from flask_login import login_required, current_user

from models.bookingData import Booking

from flask import jsonify
from datetime import datetime
from collections import defaultdict

chart = Blueprint('chart', __name__)


@chart.route('/linechart', methods=['GET', 'POST'])
@login_required
def linechart():
    if request.method == 'GET':
        return render_template('linechart.html', name=current_user.name, panel="Trend Chart")
    elif request.method == 'POST':
        testdata = request.form.get("testdata")

        xyData = {}
        # xyData is a dictionary (key:value pairs)
        # {
        #   "deluxe":[{bookingMonth1: numOfBookings1},{bookingMonth2: numOfBookings2},{bookingMonth3: umOfBookings3}],
        #   "standard":[{bookingMonth1: numOfBookings1},{bookingMonth2: numOfBookings2},...]
        # }

        AllBookingObjs = Booking.objects()
        numOfStandardBookingsByMonthDict = defaultdict(int)
        numOfDeluxeBookingsByMonthDict = defaultdict(int)
        # First, group all the bookings by roomtypes
        for booking in AllBookingObjs:
            roomType = booking.roomSet.RoomType.name  # either 'deluxe' or 'standard'

            if roomType == 'standard':
                # Second, get the months, get the numOfBookings, store them in a Dict
                checkInMonthYear = booking.checkInDate.strftime("%b %Y")
                numOfStandardBookingsByMonthDict[checkInMonthYear] += 1
                # Third, store the Dict into a list
                ListOf_numOfStandardBookingsByMonthDict = [{key: value} for key, value in
                                                           numOfStandardBookingsByMonthDict.items()]

            # repeat step 2 and 3 for deluxe room type
            elif roomType == 'deluxe':
                checkInMonthYear = booking.checkInDate.strftime("%b %Y")
                numOfDeluxeBookingsByMonthDict[checkInMonthYear] += 1
                ListOf_numOfDeluxeBookingsByMonthDict = [{key: value} for key, value in
                                                         numOfDeluxeBookingsByMonthDict.items()]

            else:
                print(f'unknown room type :{roomType}')

        # Forth, put the list of dicts as the value in the corresponding key
        xyData['deluxe'] = sorted(ListOf_numOfDeluxeBookingsByMonthDict,
                                  key=lambda x: datetime.strptime(list(x.keys())[0], "%b %Y"))
        xyData['standard'] = sorted(ListOf_numOfStandardBookingsByMonthDict,
                                    key=lambda x: datetime.strptime(list(x.keys())[0], "%b %Y"))

        print(xyData)

        return jsonify({"xyData": xyData})

//to show details of booking when a booking is clicked
$('#list-tab a').on('click', function (e) {
  e.preventDefault();
  $(this).tab('show');
});

$('#list-tab a:first-child').tab('show');

//to get bookings of the user from the passport selected
function getBookings() {
  var dropdownList = document.getElementById("passportSelect");
  var selectedIndex = dropdownList.selectedIndex;
  var selectedOption = dropdownList.options[selectedIndex];
  getBookingsFromEmail(selectedOption.value);
}
//called within the getBookings function
function getBookingsFromEmail(aEmail) {

  $.ajax({
    url: "/getBookings",
    type: "POST",
    data: {
      aEmail: aEmail
    },
    error: function() {
      alert("getBookings error!");
    }, //end of error
    success: function(resp) {
      $('div#check_in_response').html(resp.data);
      $('#list-tab a:first-child').tab('show');
    } //end of success
  }) //end of ajax call
} //end of getBookings Function
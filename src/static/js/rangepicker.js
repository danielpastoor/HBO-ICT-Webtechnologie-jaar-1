document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#weekRange", {
        mode: "range",
        minDate: "today",
        dateFormat: "Y-m-d",
        // disable: [
        //   function(date) {
        //     // Disable all days except Mondays
        //     return (date.getDay() !== 1);
        //   },
        //   }
        // ],
        onChange: function (selectedDates, dateStr) {
            document.getElementById("weekRange").value = dateStr;
        }
    });

    var bookingDateElement = document.getElementById("");

    if (bookingDateElement) {
        var disableDates = []

        var booked_dates_string = bookingDateElement.getAttribute("data-booked-dates");

        if (booked_dates_string) {
            var booked_dates = JSON.parse(booked_dates_string)

            if (booked_dates) {
                for (let i = 0; i < booked_dates.length; i++) {
                    var booked_date = booked_dates[i]

                    disableDates.push({
                        from: booked_date["start_date"],
                        to: booked_date["end_date"]
                    })
                }
            }
        }

        flatpickr("#bookingdates", {
            mode: "range",
            minDate: "today",
            inline: true,
            dateFormat: "Y-m-d",
            disable: disableDates,
            onChange: function (selectedDates, dateStr) {
                document.getElementById("bookingdates").value = dateStr;

                if (selectedDates.length > 0) {
                    document.querySelector("input[name='checkindate']").value = selectedDates[0].toISOString().substring(0, 10);

                    if (selectedDates.length > 1)
                        document.querySelector("input[name='checkoutdate']").value = selectedDates[1].toISOString().substring(0, 10);
                }
            }
        });
    }
});




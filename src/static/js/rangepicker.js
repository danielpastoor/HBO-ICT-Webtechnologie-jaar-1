document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#weekRange", {
        mode: "range",
        weekNumbers: true,
        showMonths: 2,
        minDate: "today",
        dateFormat: "Y-m-d"
    });

    var bookingDateElement = document.getElementById("bookingdates");

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
            showMonths: 2,
            inline: true,
            dateFormat: "Y-m-d",
            disable: disableDates,
        });
    }
});




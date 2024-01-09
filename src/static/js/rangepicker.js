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

    flatpickr("#bookingdates", {
        mode: "range",
        minDate: "today",
        inline: true,
        dateFormat: "Y-m-d",
        disable: [
            {
                from: "2025-04-01",
                to: "2025-05-01"
            },
            {
                from: "2025-09-01",
                to: "2025-12-01"
            }
        ],
        onChange: function (selectedDates, dateStr) {
            document.getElementById("bookingdates").value = dateStr;

            if (selectedDates.length > 0) {
                document.querySelector("input[name='checkindate']").value = selectedDates[0].toString("Y-m-d");

                if (selectedDates.length > 1)
                    document.querySelector("input[name='checkoutdate']").value = selectedDates[1].toString("Y-m-d");
            }
        }
    });
});




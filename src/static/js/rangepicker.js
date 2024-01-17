document.addEventListener('DOMContentLoaded', function () {
        flatpickr("#weekRange", {
            mode: "range",
            weekNumbers: true,
            showMonths: 2,
            minDate: "today",
            dateFormat: "Y-m-d",
            onChange: (selectedDates, dateStr, instance) => {
                var secondDate = selectedDates[1] ? selectedDates[1] : selectedDates[0];

                const diffTime = Math.abs(selectedDates[0] - secondDate);
                let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

                if (diffDays % 7 !== 0 && diffDays > 1) {
                    const newEndDate = new Date(selectedDates[0]);
                    newEndDate.setDate(newEndDate.getDate() + Math.ceil((diffDays - 2) / 7) * 7);

                    newEndDate.setDate(newEndDate.getDate() - 1)

                    instance.setDate([selectedDates[0], newEndDate], true);
                }

                if (selectedDates.length > 0) {
                    document.querySelector("input[name='start_date']").value = selectedDates[0].toISOString().substring(0, 10);

                    if (selectedDates.length > 1)
                        document.querySelector("input[name='end_date']").value = selectedDates[1].toISOString().substring(0, 10);
                }
            }
        });

        var bookingDateElement = document.getElementById("bookingdates");

        if (bookingDateElement) {
            var disableDates = []

            var booked_dates_string = bookingDateElement.getAttribute("data-booked-dates");
            var amount_per_night = bookingDateElement.getAttribute("data-amount-per-night");

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
                onChange: function (selectedDates, dateStr, instance) {
                    var secondDate = selectedDates[1] ? selectedDates[1] : selectedDates[0];

                    const diffTime = Math.abs(selectedDates[0] - secondDate);
                    let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

                    if (diffDays % 7 !== 0 && diffDays > 1) {
                        const newEndDate = new Date(selectedDates[0]);
                        newEndDate.setDate(newEndDate.getDate() + Math.ceil((diffDays - 2) / 7) * 7);

                        newEndDate.setDate(newEndDate.getDate() - 1)

                        instance.setDate([selectedDates[0], newEndDate], true);
                    }

                    if (selectedDates.length > 0) {
                        document.querySelector("input[name='start_date']").value = selectedDates[0].toISOString().substring(0, 10);

                        if (selectedDates.length > 1)
                            document.querySelector("input[name='end_date']").value = selectedDates[1].toISOString().substring(0, 10);
                    }

                    var amountField = document.getElementById("amount")

                    if (amountField) {
                        amountField.innerText = (amount_per_night * diffDays).toString();
                    }
                }
            });
        }
    }
)
;




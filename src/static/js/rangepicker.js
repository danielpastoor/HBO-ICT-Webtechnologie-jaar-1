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
    onChange: function(selectedDates, dateStr) {
      document.getElementById("weekRange").value = dateStr;
    }
  });
});

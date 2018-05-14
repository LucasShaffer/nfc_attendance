function updateDisplay() {
      var jqxhr = $.get("message.php", function(data){
            $('#Message').html(data);
      });
      var newVar = $.get("date.php", function(data){
            $('#myDate').html(data);
      });
  }
   
  $(document).ready(function() {
  // Create two variable with the names of the months and days in an array
  var monthNames = [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ];
  var dayNames= ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
   
  // Create a newDate() object
  var newDate = new Date();
  // Extract the current date from Date object
  newDate.setDate(newDate.getDate());
  // Output the day, date, month and year   
  $('#Date').html(dayNames[newDate.getDay()] + " " + newDate.getDate() + ' ' + monthNames[newDate.getMonth()] + ' ' + newDate.getFullYear());
   
  setInterval( function() {
      // Create a newDate() object and extract the seconds of the current time
      var seconds = new Date().getSeconds();
      // Add a leading zero to seconds value
      $("#sec").html(( seconds < 10 ? "0" : "" ) + seconds);
      },1000);
       
  setInterval( function() {
      // Create a newDate() object and extract the minutes of the current time
      var minutes = new Date().getMinutes();
      // Add a leading zero to the minutes value
      $("#min").html(( minutes < 10 ? "0" : "" ) + minutes);
      },1000);
       
  setInterval( function() {
      // Create a newDate() object and extract the hours of the current time
      var hours = new Date().getHours();
      // Add a leading zero to the hours value
      $("#hours").html(( hours < 10 ? "0" : "" ) + hours);
      }, 1000);    
   
  setInterval(function(){updateDisplay()}, 500);
   
  });

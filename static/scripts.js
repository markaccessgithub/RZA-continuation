const child = 8 //ticket prices
const adult = 12

//this function will filter out the unselected classes by hiding all of the other classes
function animal_class(){
  d = document.getElementById("select_id").value;
  console.log(d);
  if (d=="All") {
      document.querySelectorAll('.Mammal').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Bird').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Amphibian').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Reptile').forEach(function(el) {el.style.display = 'inline';});
  } else if (d=="Mammal") {
      document.querySelectorAll('.Mammal').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Bird').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Amphibian').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Reptile').forEach(function(el) {el.style.display = 'none';});
  } else if (d=="Bird") {
      document.querySelectorAll('.Mammal').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Bird').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Amphibian').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Reptile').forEach(function(el) {el.style.display = 'none';});
  }
  else if (d=="Amphibian") {
      document.querySelectorAll('.Mammal').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Bird').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Amphibian').forEach(function(el) {el.style.display = 'inline';});
      document.querySelectorAll('.Reptile').forEach(function(el) {el.style.display = 'none';});
  }
  else if (d=="Reptile") {
      document.querySelectorAll('.Mammal').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Bird').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Amphibian').forEach(function(el) {el.style.display = 'none';});
      document.querySelectorAll('.Reptile').forEach(function(el) {el.style.display = 'inline';});
  }
}


//this function will filter out all hotel rooms that don't meet the specifications set by the user
//by setting their display to none
function hotel_filter(){
    guests = document.getElementById("guests_id").value;
    beds = document.getElementById("beds_id").value;
    console.log(guests);
    console.log(beds);

    document.querySelectorAll('.bed_one').forEach(function(el) {el.style.display = 'none';});
    document.querySelectorAll('.bed_two').forEach(function(el) {el.style.display = 'none';});
    document.querySelectorAll('.bed_three').forEach(function(el) {el.style.display = 'none';});
    document.querySelectorAll('.bed_four').forEach(function(el) {el.style.display = 'none';})
    
    if (beds=="1") {
        document.querySelectorAll('.bed_one').forEach(function(el) {el.style.display = 'inline';});
    } else if (beds=="2") {
        document.querySelectorAll('.bed_two').forEach(function(el) {el.style.display = 'inline';});
    } else if (beds=="3") {
        document.querySelectorAll('.bed_three').forEach(function(el) {el.style.display = 'inline';});
    }
    else if (beds=="4") {
        document.querySelectorAll('.bed_four').forEach(function(el) {el.style.display = 'inline';});
    }

    if (guests=="1") {
        document.querySelectorAll('.guest_two').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_three').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_four').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_five').forEach(function(el) {el.style.display = 'none';});
    } else if (guests=="2") {
        document.querySelectorAll('.guest_one').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_three').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_four').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_five').forEach(function(el) {el.style.display = 'none';});
    } else if (guests=="3") {
        document.querySelectorAll('.guest_one').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_two').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_four').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_five').forEach(function(el) {el.style.display = 'none';});
    }
    else if (guests=="4") {
        document.querySelectorAll('.guest_one').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_two').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_three').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_five').forEach(function(el) {el.style.display = 'none';});
    }
    else if (guests=="5") {
        document.querySelectorAll('.guest_one').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_two').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_three').forEach(function(el) {el.style.display = 'none';});
        document.querySelectorAll('.guest_four').forEach(function(el) {el.style.display = 'none';});
    }

}


function reset() {
    console.log("RESET")
    document.getElementById("guests_id").value = null;
    document.getElementById("beds_id").value = null;
    document.querySelectorAll('.bed_one').forEach(function(el) {el.style.display = 'inline';});
    document.querySelectorAll('.bed_two').forEach(function(el) {el.style.display = 'inline';});
    document.querySelectorAll('.bed_three').forEach(function(el) {el.style.display = 'inline';});
    document.querySelectorAll('.bed_four').forEach(function(el) {el.style.display = 'inline';});
}

//this function will calculate the total price of each adult and child tickets
function price() {
    child_tickets = document.getElementById("child_tickets").value;
    adult_tickets = document.getElementById("adult_tickets").value;
    adult_price = (adult*adult_tickets);
    child_price = (child*child_tickets);
    total = (adult_price+child_price);
    console.log(total)
    document.getElementById("display").innerText = (`£${total}`);
}
//this code is used to initialise the dropdown menus
$(document).ready(function(){
     $('.ui.dropdown').dropdown(); })

     function nights() {
        document.getElementById("error").style.display = "none";
        x = document.getElementById("check_in").value;
        y = document.getElementById("check_out").value;

        console.log(y);
        console.log(x);

        var check_in = new Date(x);
        var check_out = new Date(y);

        console.log(check_in);
        console.log(check_out);
        if (x && y) {
            if (check_in < check_out) {
                let time_difference = check_out.getTime() - check_in.getTime();
                let days_difference = Math.round(time_difference / (1000 * 3600 * 24));
                var nights = days_difference;
                var room_price = document.getElementById("room_price_hidden").innerText;
                console.log(room_price);
                var number_price = Number(room_price);
                var total = number_price * nights;
                document.getElementById("nights").innerText = nights;
                document.getElementById("display").innerText = (`£${total}`);
                document.cookie = `total=${total}`;
            } else if (check_in >= check_out) {
                document.getElementById("error").style.display = "inline";
            }
        }
    }
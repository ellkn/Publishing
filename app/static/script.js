$(document).on("click", ".go_to_top", function(e) {
    e.preventDefault();
    $('body, html').animate({scrollTop: 0}, 800);
});

statuses = document.getElementById('status')
statuses.addEventListener()

function myFunction() {
  let input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }       
  }
}

function myFunctionUser() {
    let input, filter, table, tr, td, i;
    input = document.getElementById("myInputUser");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTableUser");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }
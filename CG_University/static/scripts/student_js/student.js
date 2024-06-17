function changeContent(index) {
  var contents = document.querySelectorAll(".content");
  var navItems = document.querySelectorAll(".student-nav-item");
    console.log("Change Contents");


  contents.forEach(function (content) {
    content.classList.remove("active");
  });

  navItems.forEach(function (item) {
    item.classList.remove("active");
  });

  var selectedContent = document.getElementById("content" + index);
  if (selectedContent) {
    selectedContent.classList.add("active");
  }


  if (index > 0 && index <= navItems.length) {
    navItems[index - 1].classList.add("active");


  }
}

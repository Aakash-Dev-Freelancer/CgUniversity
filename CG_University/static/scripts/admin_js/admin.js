function changeContent(index) {
  var contents = document.querySelectorAll(".main-sub-section");
  var navItems = document.querySelectorAll(".tab-side-nav-bar");

  var panels = ["Dashboard", "Student", "Center", "All", "Settings"];
  contents.forEach(function (content) {
    content.classList.remove("active");
  });
  navItems.forEach(function (item) {
    item.classList.remove("active");
  });

  console.log(panels[index - 1]);
  var selectedContent = document.getElementById(panels[index - 1]);
  if (selectedContent) {
    selectedContent.classList.add("active");
  }

  if (index > 0 && index <= navItems.length) {
    navItems[index - 1].classList.add("active");
  }
}

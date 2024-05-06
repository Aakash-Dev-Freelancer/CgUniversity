
        function submitForm(student) {
            // Prevent the default form submission behavior
            event.preventDefault();

            // You can add your JavaScript logic here
            // For example, you can access form data and perform validation
            // Then you can submit the form using AJAX or perform any other action
            console.log("Form submitted!");
        }

    function changeContent(index) {
  // Hide all content
  var contents = document.querySelectorAll(".content");
  contents.forEach(function (content) {
    content.classList.remove("active");
  });

  // Show the selected content
  var selectedContent = document.getElementById("content" + index);
  selectedContent.classList.add("active");
}
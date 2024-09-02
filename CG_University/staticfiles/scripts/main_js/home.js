// faq.js

document.addEventListener("DOMContentLoaded", function () {
  // Get all question elements
  const faqQuestions = document.querySelectorAll(".faq-question");

  faqQuestions.forEach((question) => {
    question.addEventListener("click", () => {
      const answer = question.nextElementSibling;
      const plusIcon = question.querySelector(".plus-icon");

      // Close all answers except the one being toggled
      document.querySelectorAll(".faq-answer").forEach((ans) => {
        if (ans !== answer) {
          ans.style.display = "none";
        }
      });

      // Reset all plus icons to '+'
      document.querySelectorAll(".plus-icon").forEach((icon) => {
        icon.textContent = "+";
      });

      // Toggle the display of the clicked answer
      if (answer.style.display === "block") {
        answer.style.display = "none";
        plusIcon.textContent = "+";
      } else {
        answer.style.display = "block";
        plusIcon.textContent = "-";
      }
    });
  });
});

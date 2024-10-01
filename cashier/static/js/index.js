window.onscroll = function () {
  var navbar = document.querySelector(".navbar");
  if (window.scrollY > 50) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
};

// Function to animate the counting
function countUp(element, target) {
  let count = 0;
  const increment = Math.ceil(target / 100); // Increment value
  const interval = setInterval(() => {
    count += increment;
    if (count >= target) {
      count = target;
      clearInterval(interval);
    }
    element.textContent = count;
  }, 20); // Adjust timing for smoother animation
}

// Intersection Observer to trigger the count
const counters = document.querySelectorAll(".counter");
const options = {
  root: null,
  rootMargin: "0px",
  threshold: 0.5, // Trigger when 50% of the element is visible
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const target = entry.target.getAttribute("data-target");
      countUp(entry.target, target);
      observer.unobserve(entry.target); // Stop observing after counting
    }
  });
}, options);

counters.forEach((counter) => {
  observer.observe(counter);
});

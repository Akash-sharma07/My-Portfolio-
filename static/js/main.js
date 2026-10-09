/* Small, dependency-free interactions used across the portfolio. */
(() => {
  const menuButton = document.querySelector(".menu-toggle");
  const menuPanel = document.querySelector(".nav-panel");

  if (menuButton && menuPanel) {
    const closeMenu = () => {
      menuButton.setAttribute("aria-expanded", "false");
      menuButton.setAttribute("aria-label", "Open navigation menu");
      menuPanel.classList.remove("is-open");
    };

    menuButton.addEventListener("click", () => {
      const isOpen = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Open navigation menu" : "Close navigation menu");
      menuPanel.classList.toggle("is-open", !isOpen);
    });

    menuPanel.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", (event) => {
      if (!menuPanel.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
  }

  const disabledLinks = document.querySelectorAll('a[aria-disabled="true"]');
  disabledLinks.forEach((link) => {
    link.addEventListener("click", (event) => event.preventDefault());
    link.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") event.preventDefault();
    });
  });

  const messageField = document.querySelector("#message");
  const messageCount = document.querySelector("#message-count");
  if (messageField && messageCount) {
    const updateMessageCount = () => { messageCount.textContent = String(messageField.value.length); };
    messageField.addEventListener("input", updateMessageCount);
    updateMessageCount();
  }

  document.querySelectorAll("form.contact-form").forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.reportValidity()) {
        event.preventDefault();
        return;
      }
      const submitButton = form.querySelector('button[type="submit"]');
      if (submitButton && !submitButton.disabled) {
        submitButton.disabled = true;
        submitButton.setAttribute("aria-label", "Sending message");
        submitButton.innerHTML = "Sending…";
      }
    });
  });

  const revealItems = document.querySelectorAll(".reveal");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (revealItems.length && "IntersectionObserver" in window && !reduceMotion) {
    document.documentElement.classList.add("motion-enabled");
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -25px 0px" });
    revealItems.forEach((item) => observer.observe(item));
  }
})();

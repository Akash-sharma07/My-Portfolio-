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
  const updateMessageCount = () => {
    if (messageField && messageCount) messageCount.textContent = String(messageField.value.length);
  };
  if (messageField && messageCount) {
    messageField.addEventListener("input", updateMessageCount);
    updateMessageCount();
  }

  document.querySelectorAll("form.contact-form").forEach((form) => {
    const status = form.querySelector("#contact-form-status");
    const submitButton = form.querySelector('button[type="submit"]');
    const buttonMarkup = submitButton ? submitButton.innerHTML : "";
    const honeypot = form.querySelector('[name="_gotcha"]');
    let isSubmitting = false;

    const showStatus = (message, kind) => {
      if (!status) return;
      status.classList.remove("flash-success", "flash-error", "flash-info");
      status.classList.add(`flash-${kind}`);
      status.textContent = message;
      status.hidden = false;
    };

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (isSubmitting) return;
      if (!form.reportValidity()) return;

      const endpoint = form.getAttribute("action") || "";
      if (endpoint.includes("YOUR_FORM_ID")) {
        showStatus("Contact form setup is incomplete. Add your Formspree form ID before sending messages.", "info");
        return;
      }

      let endpointUrl;
      try {
        endpointUrl = new URL(endpoint, window.location.href);
      } catch (_error) {
        showStatus("The contact form endpoint is invalid. Please try again later.", "error");
        return;
      }
      if (endpointUrl.protocol !== "https:" || endpointUrl.hostname !== "formspree.io" || !endpointUrl.pathname.startsWith("/f/")) {
        showStatus("The contact form endpoint must be your HTTPS Formspree form URL.", "error");
        return;
      }

      if (honeypot && honeypot.value.trim()) {
        showStatus("Your message could not be submitted. Please try again.", "error");
        return;
      }

      isSubmitting = true;
      if (submitButton) {
        submitButton.disabled = true;
        submitButton.setAttribute("aria-label", "Sending message");
        submitButton.textContent = "Sending?";
      }

      try {
        const response = await fetch(endpointUrl.href, {
          method: "POST",
          body: new FormData(form),
          headers: { Accept: "application/json" },
        });
        let result = null;
        try { result = await response.json(); } catch (_error) { /* Status code still determines success. */ }

        if (response.ok) {
          showStatus("Thanks for reaching out. Formspree received your message.", "success");
          form.reset();
          updateMessageCount();
        } else {
          const detail = result && Array.isArray(result.errors)
            ? result.errors.map((item) => item.message).filter(Boolean).join(" ")
            : "";
          showStatus(detail || (response.status === 429
            ? "The form is receiving messages too quickly. Please wait a moment and try again."
            : "Your message was not sent. Please check the form and try again."), "error");
        }
      } catch (_error) {
        showStatus("We could not reach the contact service. Please check your connection and try again.", "error");
      } finally {
        isSubmitting = false;
        if (submitButton) {
          submitButton.disabled = false;
          submitButton.removeAttribute("aria-label");
          submitButton.innerHTML = buttonMarkup;
        }
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

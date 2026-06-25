/* ----------------------------------------------------
   A to Z @ CWB Brand Suits - Interactive Logic
------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize all features
  initNavbar();
  initBrandDirectory();
  initScrollAnimations();
});

/* --- Header & Mobile Menu Logic --- */
function initNavbar() {
  const header = document.querySelector(".header");
  const menuToggle = document.querySelector(".menu-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navLinks = document.querySelectorAll(".nav-link");

  // Scroll event for styling header on scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
    updateActiveNavLink();
  });

  // Mobile menu toggle
  menuToggle.addEventListener("click", () => {
    menuToggle.classList.toggle("active");
    navMenu.classList.toggle("active");
  });

  // Close menu when clicking links
  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      menuToggle.classList.remove("active");
      navMenu.classList.remove("active");
    });
  });

  // Highlight active link based on scroll position
  function updateActiveNavLink() {
    const sections = document.querySelectorAll("section[id]");
    const scrollY = window.pageYOffset;

    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 100;
      const sectionId = current.getAttribute("id");
      
      const navLink = document.querySelector(`.nav-menu a[href*=${sectionId}]`);
      const bottomNavLink = document.querySelector(`.bottom-nav a[href*=${sectionId}]`);

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        if (navLink) {
          navLinks.forEach(link => link.classList.remove("active"));
          navLink.classList.add("active");
        }
        if (bottomNavLink) {
          document.querySelectorAll(".bottom-nav-item").forEach(item => item.classList.remove("active"));
          bottomNavLink.classList.add("active");
        }
      } else {
        if (navLink) {
          navLink.classList.remove("active");
        }
      }
    });
  }
}

/* --- Dynamic Brand Directory --- */
function initBrandDirectory() {
  const brandsContainer = document.getElementById("brands-container");

  if (!brandsContainer || !window.partnerBrands) return;

  // Initial render of all brands
  renderBrands(window.partnerBrands);
}

function renderBrands(brands) {
  const brandsContainer = document.getElementById("brands-container");
  brandsContainer.innerHTML = "";

  if (brands.length === 0) {
    brandsContainer.innerHTML = `
      <div class="no-results" style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">
        <p>No brands found in this category. We are actively onboarding new collections.</p>
      </div>
    `;
    return;
  }

  brands.forEach((brand, index) => {
    // Generate card element
    const card = document.createElement("div");
    card.className = "brand-card reveal";
    card.style.transitionDelay = `${(index % 3) * 0.1}s`;
    card.style.cursor = "pointer";

    // Navigate to brand details page unless clicking the WhatsApp updates link
    card.addEventListener("click", (e) => {
      if (e.target.closest(".brand-cta-join")) {
        return;
      }
      window.location.href = `brand.html?id=${brand.id}`;
    });

    // Construct categories HTML
    const tagsHtml = brand.categories
      .map(cat => `<span class="brand-tag">${cat}</span>`)
      .join("");

    // Construct image gallery HTML
    const galleryHtml = brand.previews
      .map(
        imgUrl => `
        <div class="brand-gallery-img">
          <img src="${imgUrl}" alt="${brand.name} Collection Preview" loading="lazy" />
        </div>
      `
      )
      .join("");

    card.innerHTML = `
      <div class="brand-card-header">
        <div class="brand-monogram">${brand.monogram}</div>
        <div class="brand-title-wrap">
          <h3 class="brand-name">${brand.name}</h3>
          <div class="brand-tags">${tagsHtml}</div>
        </div>
      </div>
      <p class="brand-desc">${brand.description}</p>
      <div class="brand-gallery">
        ${galleryHtml}
      </div>
      <div class="brand-actions">
        <a href="brand.html?id=${brand.id}" class="brand-cta-view">Explore Latest Updates</a>
        <a href="${brand.whatsappUrl}" target="_blank" class="brand-cta-join" rel="noopener noreferrer" title="Join Brand Updates">
          <span class="brand-cta-icon"><i class="fab fa-whatsapp"></i></span>
          Join Updates
        </a>
      </div>
    `;

    brandsContainer.appendChild(card);
  });

  // Re-observe newly rendered elements
  observeNewElements();
}

/* --- Scroll-driven Reveal Animations --- */
let revealObserver;

function initScrollAnimations() {
  const revealElements = document.querySelectorAll(".reveal");

  const observerOptions = {
    root: null,
    rootMargin: "0px 0px -80px 0px", // Trigger slightly before element enters view
    threshold: 0.1
  };

  revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("revealed");
        // Once revealed, no need to track it further
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach(el => revealObserver.observe(el));
}

function observeNewElements() {
  const elements = document.querySelectorAll(".brand-card.reveal");
  elements.forEach(el => {
    if (revealObserver) {
      revealObserver.observe(el);
    }
  });
}


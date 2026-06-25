/* ----------------------------------------------------
   A to Z @ Khoobsurat Point - Brand Detail Logic
------------------------------------------------------- */

document.addEventListener("DOMContentLoaded", () => {
  initBrandPage();
});

function initBrandPage() {
  // Parse brand ID from URL query parameters
  const urlParams = new URLSearchParams(window.location.search);
  const brandId = urlParams.get("id");

  const brandProfile = document.getElementById("brand-profile");
  const brandError = document.getElementById("brand-error");
  const lookbookSection = document.getElementById("lookbook-gallery-section");
  const profileWhatsapp = document.getElementById("brand-profile-whatsapp");

  // Validate presence of brand data
  if (!brandId || !window.partnerBrands) {
    showErrorState();
    return;
  }

  // Find target brand
  const brand = window.partnerBrands.find(b => b.id === brandId);
  if (!brand) {
    showErrorState();
    return;
  }

  // Brand found! Populate UI elements
  document.title = `${brand.name} Catalog Lookbook | A to Z a Khoobsurat Point`;
  
  // 1. Render scrollable brand list in Header (Desktop)
  const scrollNav = document.getElementById("brand-header-scroll-nav");
  if (scrollNav) {
    scrollNav.innerHTML = window.partnerBrands
      .map(
        b => `
        <a href="brand.html?id=${b.id}" class="brand-nav-item ${b.id === brand.id ? "active" : ""}">
          ${b.name}
        </a>
      `
      )
      .join("");

    // Center active item in scroll container horizontally
    const activeNavEl = scrollNav.querySelector(".brand-nav-item.active");
    if (activeNavEl) {
      setTimeout(() => {
        scrollNav.scrollTo({
          left: activeNavEl.offsetLeft - (scrollNav.offsetWidth / 2) + (activeNavEl.offsetWidth / 2),
          behavior: "instant"
        });
      }, 50);
    }
  }

  // 2. Render collapsed brand list dropdown (Mobile)
  const mobileDropdown = document.getElementById("brand-mobile-dropdown");
  const mobileActiveLabel = document.getElementById("brand-mobile-select-active");
  if (mobileDropdown && mobileActiveLabel) {
    mobileActiveLabel.textContent = brand.name;
    mobileDropdown.innerHTML = window.partnerBrands
      .map(
        b => `
        <a href="brand.html?id=${b.id}" class="brand-mobile-dropdown-item ${b.id === brand.id ? "active" : ""}">
          ${b.name}
        </a>
      `
      )
      .join("");

    // Toggle dropdown visibility
    const mobileWrapper = document.getElementById("brand-mobile-select-wrapper");
    const mobileSelectBtn = document.getElementById("brand-mobile-select-btn");
    
    if (mobileSelectBtn && mobileWrapper) {
      mobileSelectBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        mobileWrapper.classList.toggle("active");
      });

      // Close dropdown when clicking outside
      document.addEventListener("click", () => {
        mobileWrapper.classList.remove("active");
      });
    }
  }

  // Set WhatsApp Update link in Profile Header
  if (profileWhatsapp) {
    profileWhatsapp.href = brand.whatsappUrl;
  }

  // Set Profile Elements
  document.getElementById("brand-header-monogram").textContent = brand.monogram;
  document.getElementById("brand-profile-name").textContent = brand.name;
  document.getElementById("brand-profile-desc").textContent = brand.description;

  // Render Category Badges in Profile
  const tagsContainer = document.getElementById("brand-profile-tags");
  tagsContainer.innerHTML = brand.categories
    .map(cat => `<span class="brand-tag">${cat}</span>`)
    .join("");

  // Render Lookbook Posts
  renderLookbook(brand.posts);

  // Setup Carousel Sliders inside each card
  initCardCarousels();

  function showErrorState() {
    if (brandProfile) brandProfile.style.display = "none";
    if (lookbookSection) lookbookSection.style.display = "none";
    if (profileWhatsapp) profileWhatsapp.style.display = "none";
    if (brandError) brandError.style.display = "block";
  }
}

/* --- Render Lookbook Posts --- */
function renderLookbook(posts) {
  const grid = document.getElementById("lookbook-posts-grid");
  if (!grid) return;

  grid.innerHTML = "";

  posts.forEach((post, index) => {
    // Generate card element
    const card = document.createElement("div");
    card.className = "post-card";

    // Construct carousel slides HTML
    const slidesHtml = post.images
      .map(
        (imgUrl, idx) => `
        <div class="post-carousel-slide">
          <img src="${imgUrl}" alt="Style design ${post.number} slide ${idx + 1}" loading="lazy" />
        </div>
      `
      )
      .join("");

    // Construct tiny indicator dots HTML
    const dotsHtml = post.images
      .map(
        (_, idx) => `
        <div class="carousel-indicator-dot ${idx === 0 ? "active" : ""}" data-slide="${idx}"></div>
      `
      )
      .join("");

    card.innerHTML = `
      <div class="post-image-wrap">
        <span class="post-badge">Design ${post.number} of 9</span>
        
        <!-- Carousel scroll snaps container -->
        <div class="post-image-carousel">
          ${slidesHtml}
        </div>
        
        <!-- Instagram style indicator dots -->
        <div class="carousel-indicator-dots">
          ${dotsHtml}
        </div>
        
        <!-- Desktop Nav Arrows -->
        <button class="carousel-arrow prev" aria-label="Previous image">
          <i class="fas fa-chevron-left"></i>
        </button>
        <button class="carousel-arrow next" aria-label="Next image">
          <i class="fas fa-chevron-right"></i>
        </button>
      </div>
      
      <div class="post-details">
        <p class="post-description">${post.description}</p>
      </div>
    `;
    
    grid.appendChild(card);
  });
}

/* --- Initialize Instagram-Style Image Carousels --- */
function initCardCarousels() {
  const cards = document.querySelectorAll(".post-card");
  
  cards.forEach(card => {
    const carousel = card.querySelector(".post-image-carousel");
    const prevBtn = card.querySelector(".carousel-arrow.prev");
    const nextBtn = card.querySelector(".carousel-arrow.next");
    const dots = card.querySelectorAll(".carousel-indicator-dot");

    if (!carousel || !prevBtn || !nextBtn || dots.length === 0) return;

    // 1. Sync Active Dot Highlights on scroll
    carousel.addEventListener("scroll", () => {
      const scrollLeft = carousel.scrollLeft;
      const width = carousel.offsetWidth;
      if (width === 0) return;

      const activeIndex = Math.round(scrollLeft / width);

      // Update dots highlights
      dots.forEach((dot, idx) => {
        if (idx === activeIndex) {
          dot.classList.add("active");
        } else {
          dot.classList.remove("active");
        }
      });
    });

    // 2. Next Button Trigger click with wrap-around loop
    nextBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const width = carousel.offsetWidth;
      const scrollLeft = carousel.scrollLeft;
      const maxScroll = carousel.scrollWidth - width;

      if (scrollLeft >= maxScroll - 5) {
        carousel.scrollTo({
          left: 0,
          behavior: "smooth"
        });
      } else {
        carousel.scrollBy({
          left: width,
          behavior: "smooth"
        });
      }
    });

    // 3. Prev Button Trigger click with wrap-around loop
    prevBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const width = carousel.offsetWidth;
      const scrollLeft = carousel.scrollLeft;
      const maxScroll = carousel.scrollWidth - width;

      if (scrollLeft <= 5) {
        carousel.scrollTo({
          left: maxScroll,
          behavior: "smooth"
        });
      } else {
        carousel.scrollBy({
          left: -width,
          behavior: "smooth"
        });
      }
    });

    // 4. Tiny dots click-to-nav
    dots.forEach(dot => {
      dot.addEventListener("click", (e) => {
        e.stopPropagation();
        const targetIndex = parseInt(e.target.getAttribute("data-slide"));
        const width = carousel.offsetWidth;
        
        carousel.scrollTo({
          left: targetIndex * width,
          behavior: "smooth"
        });
      });
    });
  });
}

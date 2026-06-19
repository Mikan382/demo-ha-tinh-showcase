/**
 * Travello Template - Main JavaScript
 * Vanilla JS (no jQuery required)
 */

// ========================================
// AOS - Initialize OUTSIDE DOMContentLoaded
// (Scripts at body bottom are already deferred)
// ========================================
if (typeof AOS !== 'undefined') {
  AOS.init({
    duration: 800,
    easing: 'ease-out',
    once: true
  });

  window.addEventListener('load', function() {
    AOS.refresh();
  });
}

// ========================================
// Main Initialization
// ========================================
document.addEventListener('DOMContentLoaded', function() {
  'use strict';

  initHeader();
  initMobileMenu();
  initHomeSlider();
  initTestimonialsSlider();
  initFeaturedToursSlider();
  initGallerySlider();
  initIsotope();
  initDestinationsFilter();
  initDestinationsMap();
  initMilestoneCounters();
  initProgressBars();
  initAccordions();
  initItineraryAccordion();
  initTabs();
  initTourTabs();
  initInput();
  initMap();
  initChatWidget();
  initVideoPlay();
});

// ========================================
// Header Scroll Behavior
// ========================================
function initHeader() {
  var header = document.querySelector('.header');
  var headerSocial = document.querySelector('.header_social');
  if (!header) return;

  function setHeader() {
    if (window.scrollY > 127) {
      header.classList.add('scrolled');
      if (headerSocial) headerSocial.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
      if (headerSocial) headerSocial.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', setHeader);
  window.addEventListener('resize', setHeader);
  setHeader();
}

// ========================================
// Mobile Menu
// ========================================
function initMobileMenu() {
  var menu = document.querySelector('.menu');
  var burger = document.querySelector('.hamburger');
  var menuClose = document.querySelector('.menu_close_container');
  if (!menu || !burger) return;

  burger.addEventListener('click', function() {
    menu.classList.add('active');
  });

  if (menuClose) {
    menuClose.addEventListener('click', function() {
      menu.classList.remove('active');
    });
  }

  // Close menu on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && menu.classList.contains('active')) {
      menu.classList.remove('active');
    }
  });
}

// ========================================
// Home Slider (Swiper)
// ========================================
function initHomeSlider() {
  var el = document.querySelector('.home-slider');
  if (!el || typeof Swiper === 'undefined') return;

  new Swiper('.home-slider', {
    slidesPerView: 1,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    speed: 1200,
    effect: 'fade',
    fadeEffect: {
      crossFade: true
    }
  });
}

// ========================================
// Testimonials Slider (Swiper)
// ========================================
function initTestimonialsSlider() {
  var el = document.querySelector('.testimonials-slider');
  if (!el || typeof Swiper === 'undefined') return;

  new Swiper('.testimonials-slider', {
    slidesPerView: 1,
    loop: true,
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },
    effect: 'fade',
    fadeEffect: {
      crossFade: true
    },
    speed: 1200
  });
}

// ========================================
// Isotope Filter (destinations.html & index.html)
// ========================================
function initIsotope() {
  var grid = document.querySelector('.item_grid');
  if (!grid || typeof Isotope === 'undefined') return;

  // Wait for all images in the grid to load before initializing Isotope
  var images = grid.querySelectorAll('img');
  var loadedCount = 0;
  var totalImages = images.length;

  function initializeIsotope() {
    var iso = new Isotope(grid, {
      itemSelector: '.item',
      layoutMode: 'fitRows',
      percentPosition: true,
      getSortData: {
        price: function(el) {
          var priceText = el.querySelector('.destination_price');
          if (priceText) {
            return parseFloat(priceText.textContent.replace(/[^0-9.]/g, '')) || 0;
          }
          return 0;
        },
        name: function(el) {
          var titleEl = el.querySelector('.destination_title a');
          return titleEl ? titleEl.textContent.trim() : '';
        }
      }
    });

    // Relayout after a short delay to ensure proper positioning
    setTimeout(function() {
      iso.layout();
    }, 100);

    // Also relayout on window load (for cached images)
    window.addEventListener('load', function() {
      iso.layout();
    });

    // Sorting buttons
    var sortingBtns = document.querySelectorAll('.product_sorting_btn');
    sortingBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var optionStr = this.getAttribute('data-isotope-option');
        if (optionStr) {
          var option = JSON.parse(optionStr);
          iso.arrange(option);
        }
      });
    });

    // Region filter buttons (dropdown)
    var filterBtns = document.querySelectorAll('.filter_btn');
    filterBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var filterValue = this.getAttribute('data-filter');
        iso.arrange({ filter: filterValue });
        updateResultsCount(iso);
      });
    });

    // Category filter buttons (filter bar)
    var catBtns = document.querySelectorAll('.filter_cat_btn');
    catBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        catBtns.forEach(function(b) { b.classList.remove('active'); });
        this.classList.add('active');
        var filterValue = this.getAttribute('data-filter');
        iso.arrange({ filter: filterValue });
        updateResultsCount(iso);
      });
    });

    // Helper to update results count
    function updateResultsCount(iso) {
      var countEl = document.querySelector('.results_count strong');
      if (countEl) {
        countEl.textContent = iso.filteredItems.length;
      }
    }

    // Disable AOS on items after initial animation to prevent conflicts with Isotope
    setTimeout(function() {
      var items = grid.querySelectorAll('.item[data-aos]');
      items.forEach(function(item) {
        item.removeAttribute('data-aos');
        item.removeAttribute('data-aos-delay');
        item.classList.add('aos-animate'); // Keep the "animated" state
      });
    }, 1500);
  }

  // If no images, initialize immediately
  if (totalImages === 0) {
    initializeIsotope();
    return;
  }

  // Wait for images to load
  function onImageLoad() {
    loadedCount++;
    if (loadedCount >= totalImages) {
      initializeIsotope();
    }
  }

  images.forEach(function(img) {
    if (img.complete) {
      onImageLoad();
    } else {
      img.addEventListener('load', onImageLoad);
      img.addEventListener('error', onImageLoad); // Handle broken images
    }
  });

  // Fallback: initialize after timeout if images are slow
  setTimeout(function() {
    if (loadedCount < totalImages) {
      initializeIsotope();
    }
  }, 3000);
}

// ========================================
// Milestone Counters
// Uses IntersectionObserver (replaces GSAP/ScrollMagic)
// ========================================
function initMilestoneCounters() {
  var counters = document.querySelectorAll('.milestone_counter');
  if (!counters.length) return;

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(function(counter) {
    observer.observe(counter);
  });

  function animateCounter(el) {
    var endValue = parseInt(el.getAttribute('data-end-value'), 10);
    if (isNaN(endValue)) {
      endValue = parseInt(el.textContent, 10) || 0;
    }

    var duration = 2000;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      // Easing function for smooth animation
      var easeOut = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(easeOut * endValue);

      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = endValue;
      }
    }
    requestAnimationFrame(step);
  }
}

// ========================================
// Progress Bars (elements.html)
// Uses IntersectionObserver (replaces progressbar.js)
// ========================================
function initProgressBars() {
  var loaders = document.querySelectorAll('.loader[data-perc]');
  if (!loaders.length) return;

  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        animateProgressBar(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  loaders.forEach(function(loader) {
    observer.observe(loader);
  });

  function animateProgressBar(el) {
    var perc = parseFloat(el.getAttribute('data-perc')) || 0;
    var duration = 1500;
    var startTime = null;

    // Create SVG circle if not exists
    var existingSvg = el.querySelector('svg.progress-ring');
    if (!existingSvg) {
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'progress-ring');
      svg.setAttribute('width', '140');
      svg.setAttribute('height', '140');
      svg.style.position = 'absolute';
      svg.style.top = '0';
      svg.style.left = '50%';
      svg.style.transform = 'translateX(-50%) rotate(-90deg)';

      var circleBg = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circleBg.setAttribute('cx', '70');
      circleBg.setAttribute('cy', '70');
      circleBg.setAttribute('r', '60');
      circleBg.setAttribute('fill', 'none');
      circleBg.setAttribute('stroke', '#e4e6e8');
      circleBg.setAttribute('stroke-width', '4');

      var circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('class', 'progress-ring-circle');
      circle.setAttribute('cx', '70');
      circle.setAttribute('cy', '70');
      circle.setAttribute('r', '60');
      circle.setAttribute('fill', 'none');
      circle.setAttribute('stroke', '#181818');
      circle.setAttribute('stroke-width', '4');
      circle.setAttribute('stroke-linecap', 'round');

      var circumference = 2 * Math.PI * 60;
      circle.style.strokeDasharray = circumference;
      circle.style.strokeDashoffset = circumference;
      circle.style.transition = 'none';

      svg.appendChild(circleBg);
      svg.appendChild(circle);
      el.insertBefore(svg, el.firstChild);
    }

    var progressCircle = el.querySelector('.progress-ring-circle');
    if (!progressCircle) return;

    var circumference = 2 * Math.PI * 60;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var easeOut = 1 - Math.pow(1 - progress, 3);
      var offset = circumference - (easeOut * perc * circumference);
      progressCircle.style.strokeDashoffset = offset;

      if (progress < 1) {
        requestAnimationFrame(step);
      }
    }
    requestAnimationFrame(step);
  }
}

// ========================================
// Accordions (elements.html)
// ========================================
function initAccordions() {
  var accordions = document.querySelectorAll('.accordion');
  if (!accordions.length) return;

  accordions.forEach(function(accordion) {
    accordion.addEventListener('click', function() {
      var panel = this.nextElementSibling;
      var isActive = this.classList.contains('active');

      // Close all accordions in the same container
      var container = this.closest('.accordions');
      if (container) {
        container.querySelectorAll('.accordion').forEach(function(acc) {
          acc.classList.remove('active');
          var p = acc.nextElementSibling;
          if (p && p.classList.contains('accordion_panel')) {
            p.style.maxHeight = null;
          }
        });
      }

      // Toggle current
      if (!isActive) {
        this.classList.add('active');
        if (panel && panel.classList.contains('accordion_panel')) {
          panel.style.maxHeight = panel.scrollHeight + 'px';
        }
      }
    });
  });

  // Initialize active accordion
  accordions.forEach(function(accordion) {
    if (accordion.classList.contains('active')) {
      var panel = accordion.nextElementSibling;
      if (panel && panel.classList.contains('accordion_panel')) {
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    }
  });
}

// ========================================
// Tabs (elements.html)
// ========================================
function initTabs() {
  var tabs = document.querySelectorAll('.tabs_container .tab');
  if (!tabs.length) return;

  tabs.forEach(function(tab, index) {
    tab.addEventListener('click', function() {
      var container = this.closest('.tabs_container');
      if (!container) return;

      // Remove active from all tabs and panels
      container.querySelectorAll('.tab').forEach(function(t) {
        t.classList.remove('active');
      });
      container.querySelectorAll('.tab_panel').forEach(function(p) {
        p.classList.remove('active');
      });

      // Activate clicked tab and corresponding panel
      this.classList.add('active');
      var panels = container.querySelectorAll('.tab_panel');
      var tabIndex = Array.from(container.querySelectorAll('.tab')).indexOf(this);
      if (panels[tabIndex]) {
        panels[tabIndex].classList.add('active');
      }
    });
  });
}

// ========================================
// Input Focus Effects
// ========================================
function initInput() {
  var inputs = document.querySelectorAll('.newsletter_input, .contact_input, .inpt');
  inputs.forEach(function(input) {
    var border = input.nextElementSibling;
    if (!border || !border.classList.contains('input_border')) return;

    input.addEventListener('focus', function() {
      border.style.visibility = 'visible';
      border.style.opacity = '1';
    });

    input.addEventListener('blur', function() {
      border.style.visibility = 'hidden';
      border.style.opacity = '0';
    });
  });
}

// ========================================
// Leaflet Map (contact.html)
// ========================================
function initMap() {
  var mapContainer = document.getElementById('map');
  if (!mapContainer || typeof L === 'undefined') return;

  // Sanford, FL coordinates (matches address in footer)
  var lat = 28.8003;
  var lng = -81.2744;

  var map = L.map('map').setView([lat, lng], 14);

  // OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Add marker
  L.marker([lat, lng])
    .addTo(map)
    .bindPopup('<strong>Travello</strong><br>4124 Barnes Street<br>Sanford, FL 32771')
    .openPopup();
}

// ========================================
// Featured Tours Slider (index.html)
// ========================================
function initFeaturedToursSlider() {
  var el = document.querySelector('.featured-tours-slider');
  if (!el || typeof Swiper === 'undefined') return;

  new Swiper('.featured-tours-slider', {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
      delay: 4000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },
    breakpoints: {
      576: {
        slidesPerView: 2
      },
      992: {
        slidesPerView: 3
      },
      1200: {
        slidesPerView: 4
      }
    }
  });
}

// ========================================
// Gallery Slider (destination-single.html, tour-single.html)
// ========================================
function initGallerySlider() {
  if (typeof Swiper === 'undefined') return;

  // Support multiple gallery slider selectors
  var selectors = ['.gallery-slider', '.destination-gallery-slider'];

  selectors.forEach(function(selector) {
    var el = document.querySelector(selector);
    if (!el) return;

    new Swiper(selector, {
      slidesPerView: 1,
      spaceBetween: 0,
      loop: true,
      autoplay: {
        delay: 5000,
        disableOnInteraction: false
      },
      pagination: {
        el: selector + ' .swiper-pagination',
        clickable: true
      },
      navigation: {
        nextEl: selector + ' .swiper-button-next',
        prevEl: selector + ' .swiper-button-prev'
      }
    });
  });
}

// ========================================
// Destinations Filter Bar (destinations.html)
// ========================================
function initDestinationsFilter() {
  var filterBar = document.querySelector('.filter_bar');
  if (!filterBar) return;

  // Category filter buttons
  var catBtns = filterBar.querySelectorAll('.filter_cat_btn');
  var grid = document.querySelector('.item_grid');

  catBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      // Update active state
      catBtns.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');

      // Filter with Isotope if available
      var filterValue = this.getAttribute('data-filter');
      if (grid && typeof Isotope !== 'undefined') {
        var iso = Isotope.data(grid);
        if (iso) {
          iso.arrange({ filter: filterValue });
        }
      }
    });
  });

  // Search input
  var searchInput = filterBar.querySelector('.filter_search');
  if (searchInput && grid) {
    searchInput.addEventListener('input', function() {
      var searchTerm = this.value.toLowerCase();
      var items = grid.querySelectorAll('.item');

      items.forEach(function(item) {
        var title = item.querySelector('.destination_title');
        var text = title ? title.textContent.toLowerCase() : '';
        if (text.includes(searchTerm) || searchTerm === '') {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });

      // Relayout Isotope
      if (typeof Isotope !== 'undefined') {
        var iso = Isotope.data(grid);
        if (iso) {
          setTimeout(function() { iso.layout(); }, 100);
        }
      }
    });
  }

  // View toggle (grid/map)
  var viewBtns = filterBar.querySelectorAll('.view_toggle button');
  var gridView = document.querySelector('.destinations_grid');
  var mapView = document.getElementById('destinations-map');

  viewBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      viewBtns.forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');

      var view = this.getAttribute('data-view');
      if (view === 'map') {
        if (gridView) gridView.style.display = 'none';
        if (mapView) {
          mapView.style.display = 'block';
          // Initialize map if not already
          initDestinationsMapView();
        }
      } else {
        if (gridView) gridView.style.display = '';
        if (mapView) mapView.style.display = 'none';
      }
    });
  });
}

// ========================================
// Destinations Map View (destinations.html)
// ========================================
var destinationsMapInstance = null;

function initDestinationsMap() {
  // Map is initialized on demand when view toggle is clicked
}

function initDestinationsMapView() {
  var mapContainer = document.getElementById('destinations-map');
  if (!mapContainer || typeof L === 'undefined' || destinationsMapInstance) return;

  // World view centered
  destinationsMapInstance = L.map('destinations-map').setView([20, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(destinationsMapInstance);

  // Sample destination markers
  var destinations = [
    { name: 'Bali, Indonesia', lat: -8.4095, lng: 115.1889, price: '$1,299' },
    { name: 'Paris, France', lat: 48.8566, lng: 2.3522, price: '$1,499' },
    { name: 'Tokyo, Japan', lat: 35.6762, lng: 139.6503, price: '$1,899' },
    { name: 'Santorini, Greece', lat: 36.3932, lng: 25.4615, price: '$1,599' },
    { name: 'Machu Picchu, Peru', lat: -13.1631, lng: -72.5450, price: '$2,199' },
    { name: 'Dubai, UAE', lat: 25.2048, lng: 55.2708, price: '$1,399' }
  ];

  destinations.forEach(function(dest) {
    L.marker([dest.lat, dest.lng])
      .addTo(destinationsMapInstance)
      .bindPopup('<strong>' + dest.name + '</strong><br>From ' + dest.price);
  });

  // Invalidate size after display
  setTimeout(function() {
    destinationsMapInstance.invalidateSize();
  }, 100);
}

// ========================================
// Itinerary Accordion (destination-single.html, tour-single.html)
// ========================================
function initItineraryAccordion() {
  var items = document.querySelectorAll('.itinerary_item');
  if (!items.length) return;

  items.forEach(function(item) {
    var header = item.querySelector('.itinerary_header');
    if (!header) return;

    header.addEventListener('click', function() {
      var content = item.querySelector('.itinerary_content');
      var isActive = item.classList.contains('active');

      // Close all items in the same container
      var container = item.closest('.itinerary_accordion') || item.closest('.itinerary_list');
      if (container) {
        container.querySelectorAll('.itinerary_item').forEach(function(it) {
          it.classList.remove('active');
          var c = it.querySelector('.itinerary_content');
          if (c) c.style.maxHeight = null;
        });
      }

      // Toggle current
      if (!isActive) {
        item.classList.add('active');
        if (content) {
          content.style.maxHeight = content.scrollHeight + 'px';
        }
      }
    });
  });

  // Initialize first item as open
  var firstItem = document.querySelector('.itinerary_item.active');
  if (firstItem) {
    var content = firstItem.querySelector('.itinerary_content');
    if (content) {
      content.style.maxHeight = content.scrollHeight + 'px';
    }
  }
}

// ========================================
// Tour Tabs (tour-single.html)
// ========================================
function initTourTabs() {
  var tabBtns = document.querySelectorAll('.tour_tab_btn');
  if (!tabBtns.length) return;

  tabBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var container = this.closest('.tour_tabs');
      if (!container) return;

      var targetId = this.getAttribute('data-tab');
      if (!targetId) return;

      // Remove active from all buttons and panels
      container.querySelectorAll('.tour_tab_btn').forEach(function(b) {
        b.classList.remove('active');
      });
      container.querySelectorAll('.tour_tab_panel').forEach(function(p) {
        p.classList.remove('active');
      });

      // Activate clicked button and target panel
      this.classList.add('active');
      var targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });
}

// ========================================
// Chat Widget (contact.html)
// ========================================
function initChatWidget() {
  var chatWidget = document.querySelector('.chat_widget');
  if (!chatWidget) return;

  var toggle = chatWidget.querySelector('.chat_toggle');
  var popup = chatWidget.querySelector('.chat_popup');
  var closeBtn = chatWidget.querySelector('.chat_close');

  if (toggle && popup) {
    toggle.addEventListener('click', function() {
      popup.classList.toggle('active');
      toggle.classList.toggle('active');
    });
  }

  if (closeBtn && popup && toggle) {
    closeBtn.addEventListener('click', function() {
      popup.classList.remove('active');
      toggle.classList.remove('active');
    });
  }

  // Close on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && popup && popup.classList.contains('active')) {
      popup.classList.remove('active');
      if (toggle) toggle.classList.remove('active');
    }
  });

  // Simple chat send functionality
  var sendBtn = chatWidget.querySelector('.chat_send');
  var input = chatWidget.querySelector('.chat_input input');
  var messages = chatWidget.querySelector('.chat_messages');

  if (sendBtn && input && messages) {
    function sendMessage() {
      var text = input.value.trim();
      if (!text) return;

      // Add user message
      var msgDiv = document.createElement('div');
      msgDiv.className = 'chat_message user';
      msgDiv.innerHTML = '<p>' + escapeHtml(text) + '</p>';
      messages.appendChild(msgDiv);

      input.value = '';
      messages.scrollTop = messages.scrollHeight;

      // Simulate agent response
      setTimeout(function() {
        var responseDiv = document.createElement('div');
        responseDiv.className = 'chat_message agent';
        responseDiv.innerHTML = '<p>Thanks for your message! Our team will get back to you shortly.</p>';
        messages.appendChild(responseDiv);
        messages.scrollTop = messages.scrollHeight;
      }, 1000);
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  }
}

// Helper function to escape HTML
function escapeHtml(text) {
  var div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// ========================================
// Video Play Button (about.html)
// ========================================
function initVideoPlay() {
  var playBtns = document.querySelectorAll('.play_icon');
  if (!playBtns.length) return;

  playBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var videoUrl = this.getAttribute('href') || this.getAttribute('data-video');
      if (!videoUrl) return;

      // Create modal overlay
      var overlay = document.createElement('div');
      overlay.className = 'video_modal_overlay';
      overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:9999;display:flex;align-items:center;justify-content:center;';

      // Create close button
      var closeBtn = document.createElement('button');
      closeBtn.className = 'video_modal_close';
      closeBtn.innerHTML = '&times;';
      closeBtn.style.cssText = 'position:absolute;top:20px;right:30px;font-size:40px;color:#fff;background:none;border:none;cursor:pointer;z-index:10000;';

      // Create iframe container
      var iframeContainer = document.createElement('div');
      iframeContainer.style.cssText = 'width:80%;max-width:900px;aspect-ratio:16/9;';

      // Parse video URL for embed
      var embedUrl = getVideoEmbedUrl(videoUrl);

      var iframe = document.createElement('iframe');
      iframe.src = embedUrl;
      iframe.style.cssText = 'width:100%;height:100%;border:none;';
      iframe.setAttribute('allowfullscreen', '');
      iframe.setAttribute('allow', 'autoplay; encrypted-media');

      iframeContainer.appendChild(iframe);
      overlay.appendChild(closeBtn);
      overlay.appendChild(iframeContainer);
      document.body.appendChild(overlay);

      // Prevent body scroll
      document.body.style.overflow = 'hidden';

      // Close handlers
      function closeModal() {
        document.body.removeChild(overlay);
        document.body.style.overflow = '';
      }

      closeBtn.addEventListener('click', closeModal);
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay) closeModal();
      });
      document.addEventListener('keydown', function escHandler(e) {
        if (e.key === 'Escape') {
          closeModal();
          document.removeEventListener('keydown', escHandler);
        }
      });
    });
  });
}

// Helper to convert video URLs to embed format
function getVideoEmbedUrl(url) {
  // YouTube
  var ytMatch = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&]+)/);
  if (ytMatch) {
    return 'https://www.youtube.com/embed/' + ytMatch[1] + '?autoplay=1';
  }

  // Vimeo
  var vimeoMatch = url.match(/vimeo\.com\/(\d+)/);
  if (vimeoMatch) {
    return 'https://player.vimeo.com/video/' + vimeoMatch[1] + '?autoplay=1';
  }

  // Return original if no match
  return url;
}

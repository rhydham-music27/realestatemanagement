document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 5s
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      var bsAlert = new bootstrap.Alert(el);
      try { el.classList.remove('show'); } catch (e) {}
      try { bsAlert.close(); } catch (e) {}
    });
  }, 5000);

  // Image preview for featured image input (id or name: featured_image)
  var imgInput = document.querySelector('input[type=file][name=featured_image]');
  if (imgInput) {
    imgInput.addEventListener('change', function (e) {
      var file = e.target.files[0];
      if (!file) return;
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        e.target.value = '';
        return;
      }
      if (file.size > 5 * 1024 * 1024) { // 5MB
        alert('Image too large (max 5MB).');
        e.target.value = '';
        return;
      }
      var reader = new FileReader();
      reader.onload = function (ev) {
        // find preview img if exists, else create
        var preview = document.querySelector('#featured-image-preview');
        if (!preview) {
          preview = document.createElement('img');
          preview.id = 'featured-image-preview';
          preview.className = 'img-thumbnail mt-2';
          imgInput.parentNode.appendChild(preview);
        }
        preview.src = ev.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  // Simple price formatting (adds thousand separators while typing)
  var priceInput = document.querySelector('input[name=price]');
  if (priceInput) {
    priceInput.addEventListener('input', function (e) {
      var value = e.target.value.replace(/[^0-9.]/g, '');
      var parts = value.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      e.target.value = parts.join('.');
    });
  }

  // Character counter for description
  var desc = document.querySelector('textarea[name=description]');
  if (desc) {
    var max = desc.getAttribute('maxlength') || 2000;
    var counter = document.createElement('small');
    counter.className = 'form-text text-muted';
    desc.parentNode.appendChild(counter);
    var update = function () {
      counter.textContent = (max - desc.value.length) + ' characters remaining';
    };
    desc.addEventListener('input', update);
    update();
  }

  // Simple lightbox for gallery thumbnails
  document.querySelectorAll('.img-hover-zoom').forEach(function (thumb) {
    thumb.style.cursor = 'pointer';
    thumb.addEventListener('click', function () {
      var src = this.src;
      var modal = document.getElementById('imageLightbox');
      if (!modal) {
        modal = document.createElement('div');
        modal.id = 'imageLightbox';
        modal.className = 'modal fade';
        modal.tabIndex = -1;
        modal.innerHTML = '<div class="modal-dialog modal-dialog-centered modal-lg"><div class="modal-content"><div class="modal-body p-0"><img src="" id="lightboxImage" class="img-fluid w-100" /></div></div></div>';
        document.body.appendChild(modal);
      }
      var img = modal.querySelector('#lightboxImage');
      img.src = src;
      var bsModal = new bootstrap.Modal(modal);
      bsModal.show();
    });
  });

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
  anchor.addEventListener('click', function (e) {
    var href = this.getAttribute('href');
    if (href.length > 1) {
      var el = document.querySelector(href);
      if (el) {
        e.preventDefault();
        el.scrollIntoView({behavior: 'smooth'});
      }
    }
  });
});

// Inquiry message character counter
function initInquiryForm() {
  var inquiryMessage = document.querySelector('textarea[name="message"]');
  if (!inquiryMessage) return;

  // Character limit
  var maxLength = 500;
  inquiryMessage.maxLength = maxLength;

  // Create and append counter
  var counter = document.createElement('small');
  counter.className = 'form-text text-muted';
  inquiryMessage.parentNode.appendChild(counter);

  // Update counter function
  function updateCounter() {
    var remaining = maxLength - inquiryMessage.value.length;
    counter.textContent = remaining + ' characters remaining';
    // Change color when approaching limit
    if (remaining < 50) counter.classList.add('text-danger');
    else counter.classList.remove('text-danger');
  }

  // Event listeners
  inquiryMessage.addEventListener('input', updateCounter);
  updateCounter(); // initial count
}

// Mark inquiry as read via AJAX
function markInquiryAsRead(inquiryId, element) {
  if (!element) return;
  element.classList.remove('unread');
  // In a real implementation, send AJAX request to server
  // For MVP, we just update UI since view handles marking as read
}

// Auto-submit filter when sort changes
var sortSelect = document.querySelector('select[name="sort"]');
if (sortSelect && sortSelect.form) {
  sortSelect.addEventListener('change', function () {
    sortSelect.form.submit();
  });
}

// Initialize inquiry components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  initInquiryForm();
  
  // Handle inquiry list items
  var inquiryItems = document.querySelectorAll('.inquiry-item.unread');
  inquiryItems.forEach(function(item) {
    item.addEventListener('click', function() {
      var inquiryId = item.dataset.inquiryId;
      if (inquiryId) markInquiryAsRead(inquiryId, item);
    });
  });

  // Email link click tracking and copy
  var contactEmails = document.querySelectorAll('.contact-info a[href^="mailto:"]');
  contactEmails.forEach(function(email) {
    email.addEventListener('click', function(e) {
      // Log click if needed
      console.log('Email contact clicked:', email.href);
    });
  });

  // Keyboard shortcut: Ctrl/Cmd+F focuses on filter search input
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      var search = document.querySelector('input[name="search"]');
      if (search) {
        e.preventDefault();
        search.focus();
      }
    }
  });
});  // --- Filter enhancements for property list ---
  var filterForm = document.getElementById('filterForm');
  var sortSelect = document.querySelector('select[name="sort"]');
  if (sortSelect && sortSelect.form) {
    sortSelect.addEventListener('change', function () {
      sortSelect.form.submit();
    });
  }

  // Preserve collapse state of filter panel using sessionStorage
  var filterPanel = document.getElementById('filterPanel');
  if (filterPanel) {
    // restore state
    try {
      var open = sessionStorage.getItem('filterPanelOpen');
      if (open === '1') {
        var bsCollapse = new bootstrap.Collapse(filterPanel, {toggle:false});
        bsCollapse.show();
      }
    } catch (e) {}

    // listen for show/hide
    filterPanel.addEventListener('shown.bs.collapse', function () { try { sessionStorage.setItem('filterPanelOpen','1'); } catch(e){} });
    filterPanel.addEventListener('hidden.bs.collapse', function () { try { sessionStorage.setItem('filterPanelOpen','0'); } catch(e){} });
  }

  // Price range validation on submit
  if (filterForm) {
    filterForm.addEventListener('submit', function (e) {
      var min = parseFloat((filterForm.querySelector('input[name="min_price"]') || {value:''}).value || '');
      var max = parseFloat((filterForm.querySelector('input[name="max_price"]') || {value:''}).value || '');
      if (!isNaN(min) && !isNaN(max) && min > max) {
        e.preventDefault();
        alert('Minimum price cannot be greater than maximum price.');
        return false;
      }
    });
  }

  // Keyboard shortcut: Ctrl/Cmd+F focuses on filter search input
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      var search = document.querySelector('input[name="search"]');
      if (search) {
        e.preventDefault();
        search.focus();
      }
    }
  });
});

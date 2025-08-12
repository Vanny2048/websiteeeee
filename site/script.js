// Smooth scroll for anchor links
const anchorLinks = document.querySelectorAll('a[href^="#"]');
for (const link of anchorLinks) {
  link.addEventListener('click', (e) => {
    const targetId = link.getAttribute('href');
    if (targetId.length > 1) {
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  });
}

// Toggle venue fields when unknown is checked
const unknown = document.getElementById('venue_unknown');
const venueFields = document.querySelector('.venue-fields');
const inputs = venueFields ? venueFields.querySelectorAll('input, select') : [];

function setVenueDisabled(isDisabled) {
  if (!venueFields) return;
  venueFields.setAttribute('aria-disabled', String(isDisabled));
  inputs.forEach((el) => (el.disabled = isDisabled));
}

if (unknown) {
  setVenueDisabled(false);
  unknown.addEventListener('change', () => setVenueDisabled(unknown.checked));
}

// Year in footer
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = String(new Date().getFullYear());
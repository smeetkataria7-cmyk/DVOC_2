/**
 * DVOC Course Enquiry Form Handler
 * Submits to Google Sheets via Apps Script (same spreadsheet, "Course Enquiries" tab)
 */

const COURSE_FORM_URL = "https://script.google.com/macros/s/AKfycbwmvMZ5daJPI2xk8Kt79-kM2RNZBUPMNKOep0098K9zMDLc5821Wi5gcUkhaxS2ec-zMQ/exec";

// ── Toast notifications ──────────────────────────────────────────────────────
function showCourseToast(msg, ok) {
  let wrap = document.querySelector('.dvoc-toast-container');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.className = 'dvoc-toast-container';
    wrap.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:10px;pointer-events:none';
    document.body.appendChild(wrap);
  }
  const t = document.createElement('div');
  t.style.cssText = `background:#fff;border-radius:12px;padding:14px 20px;box-shadow:0 6px 24px rgba(0,0,0,0.13);display:flex;align-items:center;gap:10px;font-family:'Poppins',sans-serif;font-size:13.5px;font-weight:500;color:#222;border-left:4px solid ${ok ? '#E87E26' : '#e53935'};min-width:260px;pointer-events:auto;transform:translateX(80px);opacity:0;transition:all .35s cubic-bezier(.175,.885,.32,1.275)`;
  t.innerHTML = `<span style="font-size:18px">${ok ? '&#10003;' : '&#9888;'}</span><span>${msg}</span>`;
  wrap.appendChild(t);
  requestAnimationFrame(() => { t.style.transform = 'translateX(0)'; t.style.opacity = '1'; });
  setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(80px)'; setTimeout(() => t.remove(), 400); }, 4000);
}

// ── Loading button state ─────────────────────────────────────────────────────
const btnStyle = `
  .btn-enroll.loading,.btn-submit.loading{opacity:.7;cursor:not-allowed;position:relative;color:transparent!important;}
  .btn-enroll.loading::after,.btn-submit.loading::after{content:'';position:absolute;width:18px;height:18px;top:50%;left:50%;margin:-9px 0 0 -9px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;animation:dvoc-spin .8s linear infinite;}
  @keyframes dvoc-spin{to{transform:rotate(360deg)}}
`;
const styleEl = document.createElement('style');
styleEl.innerHTML = btnStyle;
document.head.appendChild(styleEl);

// ── Form submit handler ──────────────────────────────────────────────────────
async function handleCourseEnquiry(e) {
  e.preventDefault();
  const form = e.target;
  const btn  = form.querySelector('button[type="submit"], .btn-enroll');

  const name   = (form.querySelector('[name="name"]')?.value   || '').trim();
  const phone  = (form.querySelector('[name="phone"]')?.value  || '').trim();
  const email  = (form.querySelector('[name="email"]')?.value  || '').trim();
  const course = (form.querySelector('[name="course"]')?.value || document.title.replace(' | DVOC INSTITUTE','') || '').trim();
  const branch = (form.querySelector('[name="branch"]')?.value || '').trim();

  // Validation
  if (!name)  return showCourseToast('Please enter your name.', false);
  if (!/^\+?\d{10,14}$/.test(phone.replace(/[\s-]/g, '')))
              return showCourseToast('Please enter a valid 10-digit phone number.', false);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
              return showCourseToast('Please enter a valid email address.', false);

  // Loading state
  if (btn) { btn.classList.add('loading'); btn.disabled = true; }

  const params = new URLSearchParams({
    name, phone, email, course, branch,
    source: 'course-page',
    timestamp: new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })
  });

  try {
    await fetch(COURSE_FORM_URL, { method: 'POST', mode: 'no-cors', body: params });
    showCourseToast("Thank you! We'll contact you shortly.", true);
    form.reset();
  } catch (err) {
    showCourseToast('Something went wrong. Please try again.', false);
  } finally {
    if (btn) { btn.classList.remove('loading'); btn.disabled = false; }
  }
}

// ── Init ─────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('#course-enquiry-form, #enquiry-form, #expert-enquiry-form');
  forms.forEach(form => form.addEventListener('submit', handleCourseEnquiry));
});

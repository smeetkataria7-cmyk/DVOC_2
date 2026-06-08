/**
 * DVOC Enquiry Form - Google Form Integration Handler
 * 
 * Instructions:
 * 1. Open Google Forms, create a form with fields matching Name, Email, Phone, Preferred Branch, I am a..., and Course.
 * 2. Get the form submission action URL (ends with "/formResponse").
 * 3. Inspect the form inputs in your browser to get the entry IDs (e.g. entry.123456789).
 * 4. Fill in the configuration below.
 */

const GOOGLE_FORM_CONFIG = {
  // Replace with your Google Form action URL
  // Example: 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSfXXXXXXXXXXXXX/formResponse'
  formUrl: '', 

  // Map your HTML field "name" attributes to Google Form input entry IDs
  fields: {
    name: 'entry.XXXXXX1',       // Replace with Name Entry ID
    email: 'entry.XXXXXX2',      // Replace with Email Entry ID
    phone: 'entry.XXXXXX3',      // Replace with Phone Entry ID
    branch: 'entry.XXXXXX4',     // Replace with Preferred Branch Entry ID
    userType: 'entry.XXXXXX5',   // Replace with User Type ("I am a...") Entry ID (only on homepage)
    course: 'entry.XXXXXX6'      // Replace with Course Name Entry ID (only on course pages)
  }
};

// Inject CSS styles for Toast Notification & Validation Errors
const injectStyles = () => {
  const css = `
    /* Toast container */
    .dvoc-toast-container {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 12px;
      pointer-events: none;
    }
    
    /* Toast Card (Glassmorphic) */
    .dvoc-toast {
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 12px;
      padding: 16px 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
      display: flex;
      align-items: center;
      gap: 12px;
      transform: translateX(100px);
      opacity: 0;
      pointer-events: auto;
      transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.4s;
      max-width: 350px;
    }
    
    .dvoc-toast.show {
      transform: translateX(0);
      opacity: 1;
    }
    
    .dvoc-toast-icon {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: bold;
      flex-shrink: 0;
    }
    
    .dvoc-toast-success .dvoc-toast-icon {
      background: #E87E26;
      color: #fff;
    }
    
    .dvoc-toast-error .dvoc-toast-icon {
      background: #ea4335;
      color: #fff;
    }
    
    .dvoc-toast-text {
      font-size: 13.5px;
      color: #1c1c1e;
      font-weight: 500;
      line-height: 1.4;
      font-family: 'Poppins', sans-serif;
    }
    
    /* Loading button state */
    .btn-submit.loading, .btn-enroll.loading {
      opacity: 0.7;
      cursor: not-allowed;
      position: relative;
      color: transparent !important;
    }
    .btn-submit.loading::after, .btn-enroll.loading::after {
      content: "";
      position: absolute;
      width: 18px;
      height: 18px;
      top: 50%;
      left: 50%;
      margin-top: -9px;
      margin-left: -9px;
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-top-color: #fff;
      border-radius: 50%;
      animation: dvoc-spin 0.8s linear infinite;
    }
    
    @keyframes dvoc-spin {
      to { transform: rotate(360deg); }
    }
  `;
  const style = document.createElement('style');
  style.innerHTML = css;
  document.head.appendChild(style);
};

// Create Toast Toast Notification helper
const showToast = (message, type = 'success') => {
  let container = document.querySelector('.dvoc-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'dvoc-toast-container';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  toast.className = `dvoc-toast dvoc-toast-${type}`;
  
  const icon = document.createElement('div');
  icon.className = 'dvoc-toast-icon';
  icon.innerHTML = type === 'success' ? '✓' : '!';
  
  const text = document.createElement('div');
  text.className = 'dvoc-toast-text';
  text.innerText = message;
  
  toast.appendChild(icon);
  toast.appendChild(text);
  container.appendChild(toast);
  
  // Trigger animation frame
  setTimeout(() => toast.classList.add('show'), 10);
  
  // Remove toast after 4 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 400);
  }, 4000);
};

// Form submission handler
const handleFormSubmit = async (e) => {
  e.preventDefault();
  const form = e.target;
  const submitBtn = form.querySelector('button');
  
  // Extract values
  const name = form.querySelector('[name="name"]')?.value.trim() || '';
  const email = form.querySelector('[name="email"]')?.value.trim() || '';
  const phone = form.querySelector('[name="phone"]')?.value.trim() || '';
  const branch = form.querySelector('[name="branch"]')?.value || '';
  const userType = form.querySelector('[name="userType"]')?.value || '';
  const course = form.querySelector('[name="course"]')?.value || '';

  // Validation checks
  if (!name) {
    showToast('Please enter your name.', 'error');
    return;
  }
  if (!phone || phone.length < 10 || !/^\+?\d{10,14}$/.test(phone.replace(/[\s-]/g, ''))) {
    showToast('Please enter a valid phone number.', 'error');
    return;
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showToast('Please enter a valid email address.', 'error');
    return;
  }
  if (!branch) {
    showToast('Please select a preferred branch.', 'error');
    return;
  }
  if (form.querySelector('[name="userType"]') && !userType) {
    showToast('Please select your profile status.', 'error');
    return;
  }

  // Set loading state
  submitBtn.classList.add('loading');
  submitBtn.disabled = true;

  // Prepare submission data
  const formData = new URLSearchParams();
  
  if (name) formData.append(GOOGLE_FORM_CONFIG.fields.name, name);
  if (email) formData.append(GOOGLE_FORM_CONFIG.fields.email, email);
  if (phone) formData.append(GOOGLE_FORM_CONFIG.fields.phone, phone);
  if (branch) formData.append(GOOGLE_FORM_CONFIG.fields.branch, branch);
  if (userType) formData.append(GOOGLE_FORM_CONFIG.fields.userType, userType);
  if (course) formData.append(GOOGLE_FORM_CONFIG.fields.course, course);

  // Submit to Google Form
  try {
    if (!GOOGLE_FORM_CONFIG.formUrl) {
      // If formUrl is not configured yet, simulate a delay and print details in the console
      console.warn("GOOGLE_FORM_CONFIG.formUrl is not set. Simulating form submission.");
      console.log("Submitted Data:", { name, email, phone, branch, userType, course });
      
      await new Promise(resolve => setTimeout(resolve, 1200));
      showToast('Thank you! Your enquiry has been received.', 'success');
      form.reset();
    } else {
      // POST request to Google Form
      await fetch(GOOGLE_FORM_CONFIG.formUrl, {
        method: 'POST',
        mode: 'no-cors', // Essential to bypass CORS blockages
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString()
      });
      
      showToast('Thank you! Your enquiry has been received.', 'success');
      form.reset();
    }
  } catch (error) {
    console.error('Error submitting form:', error);
    showToast('An error occurred. Please try again.', 'error');
  } finally {
    // Reset button loading state
    submitBtn.classList.remove('loading');
    submitBtn.disabled = false;
  }
};

// Initialize listeners on page load
document.addEventListener('DOMContentLoaded', () => {
  injectStyles();
  
  const forms = document.querySelectorAll('#enquiry-form, #expert-enquiry-form, #course-enquiry-form');
  forms.forEach(form => {
    form.addEventListener('submit', handleFormSubmit);
  });
});

// Theme toggle, form validation, and UX helpers
(function(){
  const root = document.documentElement;
  const stored = localStorage.getItem('theme');
  if (stored) root.setAttribute('data-bs-theme', stored);

  document.addEventListener('click', (e)=>{
    const btn = e.target.closest('#themeToggle');
    if (!btn) return;
    const current = root.getAttribute('data-bs-theme') || 'light';
    const next = current === 'light' ? 'dark' : 'light';
    root.setAttribute('data-bs-theme', next);
    localStorage.setItem('theme', next);
    btn.querySelector('span').textContent = next === 'light' ? 'Dark' : 'Light';
  });

  // Bootstrap client-side validation
  const forms = document.querySelectorAll('form.needs-validation');
  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });

  // Auto-dismiss alerts
  setTimeout(()=>{
    document.querySelectorAll('.alert').forEach(a=>{
      a.classList.add('fade','show');
      setTimeout(()=> a.remove(), 1200);
    });
  }, 3500);
})();

// myblog/static/myblog/js/app.js
document.addEventListener("DOMContentLoaded", () => {
  // 1. Dismiss flash alerts smoothly
  document.querySelectorAll(".alert__close").forEach((btn) => {
    btn.addEventListener("click", () => {
      const alertEl = btn.closest(".alert");
      if (!alertEl) return;
      alertEl.style.opacity = "0";
      alertEl.style.transform = "translateY(-4px)";
      setTimeout(() => alertEl.remove(), 180);
    });
  });

  // 2. Auto-suggest slug from title when creating a post (if slug field is empty)
  const titleInput = document.getElementById("id_title");
  const slugInput = document.getElementById("id_slug");

  if (titleInput && slugInput && !slugInput.dataset.manualEdited) {
    let slugTouchedByUser = Boolean(slugInput.value.trim());

    slugInput.addEventListener("input", () => {
      slugTouchedByUser = Boolean(slugInput.value.trim());
    });

    titleInput.addEventListener("input", () => {
      if (slugTouchedByUser) return;
      const generated = titleInput.value
        .toLowerCase()
        .trim()
        .replace(/[^a-z0-9\s-]/g, "")
        .replace(/\s+/g, "-")
        .replace(/-+/g, "-");
      slugInput.value = generated;
    });
  }

  // 3. Extra confirmation guard on delete buttons
  document.querySelectorAll("[data-confirm-delete]").forEach((el) => {
    el.addEventListener("click", (e) => {
      const postTitle = el.getAttribute("data-confirm-delete") || "this post";
      const ok = window.confirm(`Are you sure you want to delete "${postTitle}"?`);
      if (!ok) {
        e.preventDefault();
      }
    });
  });
});
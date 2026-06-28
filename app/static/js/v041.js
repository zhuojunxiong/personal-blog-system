(function () {
  function initFlashAutoDismiss() {
    document.querySelectorAll("[data-v041-flash]").forEach(function (item) {
      window.setTimeout(function () {
        item.style.opacity = "0";
        item.style.transform = "translateY(-6px)";
        window.setTimeout(function () {
          item.remove();
        }, 180);
      }, 4200);
    });
  }

  function initConfirmDialog() {
    var backdrop = document.querySelector("[data-v041-confirm-backdrop]");
    if (!backdrop) {
      return;
    }

    var title = backdrop.querySelector("[data-v041-confirm-title]");
    var message = backdrop.querySelector("[data-v041-confirm-message]");
    var cancel = backdrop.querySelector("[data-v041-confirm-cancel]");
    var ok = backdrop.querySelector("[data-v041-confirm-ok]");
    var pendingForm = null;

    function closeDialog() {
      backdrop.classList.remove("is-open");
      backdrop.setAttribute("aria-hidden", "true");
      pendingForm = null;
    }

    document.querySelectorAll("[data-v041-confirm]").forEach(function (trigger) {
      trigger.addEventListener("click", function (event) {
        var form = trigger.closest("form");
        if (!form) {
          return;
        }
        event.preventDefault();
        pendingForm = form;
        title.textContent = trigger.getAttribute("data-v041-confirm-title") || "确认操作";
        message.textContent = trigger.getAttribute("data-v041-confirm") || "确定要继续吗？";
        backdrop.classList.add("is-open");
        backdrop.setAttribute("aria-hidden", "false");
        cancel.focus();
      });
    });

    cancel.addEventListener("click", closeDialog);
    backdrop.addEventListener("click", function (event) {
      if (event.target === backdrop) {
        closeDialog();
      }
    });
    ok.addEventListener("click", function () {
      if (pendingForm) {
        pendingForm.submit();
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && backdrop.classList.contains("is-open")) {
        closeDialog();
      }
    });
  }

  function showMessage(message) {
    var wrap = document.querySelector(".v041-flash-wrap");
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "v041-flash-wrap";
      wrap.setAttribute("aria-live", "polite");
      wrap.setAttribute("aria-atomic", "true");
      document.body.appendChild(wrap);
    }

    var item = document.createElement("div");
    item.className = "v041-flash v041-flash-warning";
    item.setAttribute("data-v041-flash", "");
    item.setAttribute("role", "status");
    item.textContent = message;
    wrap.appendChild(item);
    window.setTimeout(function () {
      item.style.opacity = "0";
      item.style.transform = "translateY(-6px)";
      window.setTimeout(function () {
        item.remove();
      }, 180);
    }, 3200);
  }

  function initSearchForms() {
    document.querySelectorAll("[data-v041-search-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        var input = form.querySelector("[data-v041-search-input]");
        if (input && input.value.trim() === "") {
          event.preventDefault();
          showMessage("请输入搜索内容。");
          input.focus();
          return;
        }

        var button = form.querySelector("[data-v041-loading-label]");
        if (button) {
          button.dataset.v041OriginalLabel = button.textContent;
          button.textContent = button.getAttribute("data-v041-loading-label");
          button.disabled = true;
        }
      });
    });
  }

  function initAiPlaceholders() {
    document.querySelectorAll("[data-v041-ai-unavailable]").forEach(function (button) {
      button.addEventListener("click", function () {
        showMessage("AI 阅读提示功能将在后续版本开放。");
      });
    });
  }

  function initBackToSearch() {
    document.querySelectorAll("[data-v041-back-search]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        if (document.referrer && document.referrer.indexOf("/search") !== -1) {
          event.preventDefault();
          window.history.back();
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFlashAutoDismiss();
    initConfirmDialog();
    initSearchForms();
    initAiPlaceholders();
    initBackToSearch();
  });
})();

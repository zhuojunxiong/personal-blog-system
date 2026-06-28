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

  function initAuthForms() {
    document.querySelectorAll("[data-v041-auth-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        var fields = Array.prototype.slice.call(form.querySelectorAll("[data-v041-required]"));
        for (var index = 0; index < fields.length; index += 1) {
          var field = fields[index];
          if (field.value.trim() === "") {
            event.preventDefault();
            showMessage(field.getAttribute("data-v041-required") || "请完整填写表单。");
            field.focus();
            return;
          }
        }

        var password = form.querySelector("input[name='password']");
        if (password && password.hasAttribute("minlength") && password.value.length < Number(password.getAttribute("minlength"))) {
          event.preventDefault();
          showMessage("密码至少需要 6 位。");
          password.focus();
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

  function initPasswordModal() {
    var modal = document.querySelector("[data-v041-password-modal]");
    if (!modal) {
      return;
    }

    function openModal() {
      modal.classList.add("is-open");
      modal.setAttribute("aria-hidden", "false");
      var firstInput = modal.querySelector("input");
      if (firstInput) {
        firstInput.focus();
      }
    }

    function closeModal() {
      modal.classList.remove("is-open");
      modal.setAttribute("aria-hidden", "true");
    }

    document.querySelectorAll("[data-v041-open-password]").forEach(function (button) {
      button.addEventListener("click", openModal);
    });
    document.querySelectorAll("[data-v041-close-password]").forEach(function (button) {
      button.addEventListener("click", closeModal);
    });
    modal.addEventListener("click", function (event) {
      if (event.target === modal) {
        closeModal();
      }
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && modal.classList.contains("is-open")) {
        closeModal();
      }
    });
  }

  function initWritePage() {
    var form = document.querySelector("[data-v041-write-form]");
    if (!form) {
      return;
    }

    var title = form.querySelector("[data-v041-write-title]");
    var content = form.querySelector("[data-v041-write-content]");
    var category = form.querySelector("[data-v041-write-category]");
    var status = document.querySelector("[data-v041-save-status]");
    var dirty = false;
    var submitting = false;

    function setDirty(value) {
      dirty = value;
      if (!status) {
        return;
      }
      status.classList.toggle("is-dirty", value);
      status.classList.toggle("is-saved", !value && status.textContent.trim() === "已保存");
      if (value) {
        status.textContent = "未保存";
      }
    }

    form.querySelectorAll("input, textarea, select").forEach(function (field) {
      field.addEventListener("input", function () {
        setDirty(true);
      });
      field.addEventListener("change", function () {
        setDirty(true);
      });
    });

    form.addEventListener("submit", function (event) {
      var submitter = event.submitter;
      if (title && title.value.trim() === "") {
        event.preventDefault();
        showMessage("标题不能为空。");
        title.focus();
        return;
      }
      if (content && content.value.trim() === "") {
        event.preventDefault();
        showMessage("内容不能为空。");
        content.focus();
        return;
      }
      if (category && category.value.trim() === "") {
        event.preventDefault();
        showMessage("请选择文章分类。");
        category.focus();
        return;
      }

      submitting = true;
      dirty = false;
      if (status) {
        status.textContent = submitter && submitter.hasAttribute("data-v041-submit-publish") ? "发布中" : "保存中";
        status.classList.remove("is-dirty", "is-saved");
      }
      if (submitter && submitter.hasAttribute("data-v041-loading-label")) {
        if (submitter.name) {
          var submitterValue = form.querySelector("input[type='hidden'][data-v041-submit-value]");
          if (!submitterValue) {
            submitterValue = document.createElement("input");
            submitterValue.type = "hidden";
            submitterValue.setAttribute("data-v041-submit-value", "");
            form.appendChild(submitterValue);
          }
          submitterValue.name = submitter.name;
          submitterValue.value = submitter.value;
        }
        submitter.dataset.v041OriginalLabel = submitter.textContent;
        submitter.textContent = submitter.getAttribute("data-v041-loading-label");
        submitter.disabled = true;
      }
    });

    window.addEventListener("beforeunload", function (event) {
      if (!dirty || submitting) {
        return;
      }
      event.preventDefault();
      event.returnValue = "";
    });
  }

  function initWriteAiChat() {
    document.querySelectorAll("[data-v041-ai-chat]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var input = form.querySelector("input[name='question']");
        var messages = document.querySelector("[data-v041-ai-messages]");
        var text = input ? input.value.trim() : "";
        if (!text) {
          showMessage("请输入想问的问题。");
          if (input) {
            input.focus();
          }
          return;
        }

        if (messages) {
          var userMessage = document.createElement("div");
          userMessage.className = "write-ai-message is-user";
          userMessage.textContent = text;
          messages.appendChild(userMessage);

          var aiMessage = document.createElement("div");
          aiMessage.className = "write-ai-message is-ai";
          aiMessage.textContent = "AI 功能将在后续版本开放。";
          messages.appendChild(aiMessage);
          messages.scrollTop = messages.scrollHeight;
        }
        if (input) {
          input.value = "";
        }
        showMessage("AI 功能将在后续版本开放。");
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFlashAutoDismiss();
    initConfirmDialog();
    initSearchForms();
    initAuthForms();
    initAiPlaceholders();
    initBackToSearch();
    initPasswordModal();
    initWritePage();
    initWriteAiChat();
  });
})();

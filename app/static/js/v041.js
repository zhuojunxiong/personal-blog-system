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

  function escapeHtml(text) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
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

  function initAiSearch() {
    document.querySelectorAll("[data-v041-ai-search-form]").forEach(function (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        var input = form.querySelector("[data-v041-search-input]");
        var query = input ? input.value.trim() : "";
        if (!query) {
          showMessage("请输入搜索内容。");
          if (input) input.focus();
          return;
        }

        var resultsContainer = document.querySelector("[data-v041-ai-search-results]");
        var understandingEl = document.querySelector("[data-v041-ai-understanding]");
        var metaEl = document.querySelector("[data-v041-ai-search-meta]");
        var paginationEl = document.querySelector("[data-v041-ai-pagination]");
        var button = form.querySelector("[data-v041-loading-label]");

        if (resultsContainer) {
          resultsContainer.innerHTML =
            '<div class="v041-state" role="status"><div class="v041-state-inner">' +
            '<span class="v041-loading-dot" aria-hidden="true"></span>' +
            '<p class="v041-state-text">AI 正在理解你的问题并搜索相关内容…</p></div></div>';
        }
        if (understandingEl) understandingEl.style.display = "none";
        if (metaEl) metaEl.style.display = "none";
        if (paginationEl) paginationEl.innerHTML = "";

        if (button) {
          button.dataset.v041OriginalLabel = button.textContent;
          button.textContent = button.getAttribute("data-v041-loading-label") || "AI 思考中…";
          button.disabled = true;
        }

        var csrfMeta = document.querySelector('meta[name="csrf-token"]');
        var url = form.getAttribute("action") || form.dataset.v041AiSearchUrl || "/ai/search";
        var page = parseInt((form.querySelector('[name="page"]') || {}).value || "1", 10) || 1;
        var pageSize = parseInt((form.querySelector('[name="pageSize"]') || {}).value || "5", 10) || 5;

        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfMeta ? csrfMeta.getAttribute("content") : ""
          },
          body: JSON.stringify({ query: query, page: page, page_size: pageSize })
        })
          .then(function (response) {
            return response.json().then(function (data) {
              if (!response.ok || !data.ok) {
                throw new Error(data.message || "AI 搜索请求失败。");
              }
              return data;
            });
          })
          .then(function (data) {
            // 首页没有结果展示区，跳转到搜索页展示结果
            if (!document.querySelector("[data-v041-ai-search-results]")) {
              window.location.href = "/search?q=" + encodeURIComponent(query) + "&ai=1";
              return;
            }
            renderAiSearchResults(data, query, form);
          })
          .catch(function () {
            showMessage("AI 搜索暂时不可用，已切换为普通搜索。");
            var traditionalUrl = "/search?q=" + encodeURIComponent(query) +
              "&page=" + page + "&pageSize=" + pageSize;
            window.location.href = traditionalUrl;
          })
          .finally(function () {
            if (button) {
              button.textContent = button.dataset.v041OriginalLabel || "AI 搜索";
              button.disabled = false;
            }
          });
      });
    });

    // 搜索页自动触发：URL 带 ai=1 且已有 q 参数
    if (window.location.search.indexOf("ai=1") !== -1) {
      var params = new URLSearchParams(window.location.search);
      var autoQuery = params.get("q");
      if (autoQuery && autoQuery.trim()) {
        var form = document.querySelector("[data-v041-ai-search-form]");
        if (form) {
          var input = form.querySelector("[data-v041-search-input]");
          if (input) input.value = autoQuery.trim();
          form.dispatchEvent(new Event("submit", { cancelable: true }));
        }
      }
    }
  }

  function renderAiSearchResults(data, query, form) {
    var understandingEl = document.querySelector("[data-v041-ai-understanding]");
    var metaEl = document.querySelector("[data-v041-ai-search-meta]");
    var resultsContainer = document.querySelector("[data-v041-ai-search-results]");
    var paginationEl = document.querySelector("[data-v041-ai-pagination]");

    if (window.history && window.history.replaceState) {
      var newUrl = window.location.pathname + "?q=" + encodeURIComponent(query) + "&ai=1";
      window.history.replaceState({}, "", newUrl);
    }

    if (understandingEl && data.understanding) {
      understandingEl.textContent = data.understanding;
      understandingEl.style.display = "block";
    }

    if (metaEl) {
      metaEl.innerHTML = "<p>关于「" + escapeHtml(query) + "」共找到 " + data.total + " 篇相关内容。";
      if (data.fallback) {
        metaEl.innerHTML += " <small>（AI 重排序暂不可用，显示关键词匹配结果）</small>";
      }
      metaEl.innerHTML += "</p>";
      metaEl.style.display = "block";
    }

    if (resultsContainer) {
      if (data.results && data.results.length > 0) {
        var html = '<section class="search-result-list" aria-label="搜索结果列表">';
        data.results.forEach(function (item) {
          var article = item.article;
          var summary = article.ai_search_summary || article.summary || "";
          if (summary.length >= 140) summary = summary.substring(0, 137) + "...";
          var authorName = article.author || "";
          var avatarText = article.author_avatar || (authorName ? authorName.charAt(0) : "?");
          var profileUrl = article.user_id ? "/users/" + article.user_id : "#";
          var articleUrl = "/articles/" + (article.slug || "");

          html +=
            '<article class="search-result-card">' +
              '<a class="search-result-author" href="' + profileUrl + '">' +
                '<span class="search-author-avatar">' + escapeHtml(avatarText) + '</span>' +
                '<span>作者 ' + escapeHtml(authorName) + '</span>' +
              '</a>' +
              '<a class="search-result-body" href="' + articleUrl + '">' +
                '<h2>' + escapeHtml(article.title) + '</h2>' +
                '<span class="search-ai-label">搜索摘要</span>';
          if (item.reason) {
            html += '<span class="ai-search-reason">' + escapeHtml(item.reason) + '</span>';
          }
          if (item.relevance > 0) {
            html += '<span class="ai-search-relevance">相关性 ' + Math.round(item.relevance * 100) + '%</span>';
          }
          html += '<p>' + escapeHtml(summary) + '</p>' +
              '</a>' +
            '</article>';
        });
        html += '</section>';
        resultsContainer.innerHTML = html;
      } else {
        resultsContainer.innerHTML =
          '<div class="v041-state" role="status"><div class="v041-state-inner">' +
          '<span class="v041-state-icon" aria-hidden="true">空</span>' +
          '<h2 class="v041-state-title">没有找到相关内容</h2>' +
          '<p class="v041-state-text">试试用其他方式描述你的需求。</p></div></div>';
      }
    }

    if (paginationEl) {
      paginationEl.innerHTML = "";
    }
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
        var shell = document.querySelector("[data-v041-write-page]");
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
          aiMessage.textContent = "思考中...";
          messages.appendChild(aiMessage);
          messages.scrollTop = messages.scrollHeight;
          requestAi(shell ? shell.dataset.aiChatUrl : "", {
            question: text,
            content: getWriteContent(),
            article_id: shell ? shell.dataset.aiArticleId : ""
          }).then(function (data) {
            aiMessage.textContent = data.result;
          }).catch(function (error) {
            aiMessage.textContent = error.message;
            showMessage(error.message);
          }).finally(function () {
            messages.scrollTop = messages.scrollHeight;
          });
        }
        if (input) {
          input.value = "";
        }
      });
    });
  }

  function initReadingAssistant() {
    var shell = document.querySelector("[data-v041-reading-page]");
    if (!shell) {
      return;
    }
    var output = document.querySelector("[data-v041-reading-output]");
    var buttons = Array.prototype.slice.call(document.querySelectorAll("[data-v041-reading-action]"));
    var questionForm = document.querySelector("[data-v041-reading-question]");
    var questionInput = questionForm ? questionForm.querySelector("textarea[name='question']") : null;

    function setOutput(text, state) {
      if (!output) {
        return;
      }
      output.classList.toggle("is-loading", state === "loading");
      output.classList.toggle("is-error", state === "error");
      output.textContent = text;
    }

    function setBusy(value) {
      buttons.forEach(function (button) {
        button.disabled = value;
      });
      if (questionForm) {
        var submit = questionForm.querySelector("button[type='submit']");
        if (submit) submit.disabled = value;
      }
    }

    function runReadingAction(mode, question) {
      var url = shell.dataset.aiReadingUrl || "";
      var slug = shell.dataset.articleSlug || "";
      setBusy(true);
      setOutput("AI 正在阅读这篇文章...", "loading");
      return requestAi(url, {
        slug: slug,
        mode: mode,
        question: question || ""
      }).then(function (data) {
        setOutput(data.result || "AI 没有返回内容。", "success");
      }).catch(function (error) {
        setOutput(error.message, "error");
        showMessage(error.message);
      }).finally(function () {
        setBusy(false);
      });
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        runReadingAction(button.getAttribute("data-v041-reading-action"), "");
      });
    });

    if (questionForm) {
      questionForm.addEventListener("submit", function (event) {
        event.preventDefault();
        var question = questionInput ? questionInput.value.trim() : "";
        if (!question) {
          showMessage("请输入想问文章的问题。");
          if (questionInput) questionInput.focus();
          return;
        }
        runReadingAction("question", question);
      });
    }
  }

  function initWriteAiActions() {
    document.querySelectorAll("[data-v041-ai-action]").forEach(function (button) {
      button.addEventListener("click", function () {
        var shell = document.querySelector("[data-v041-write-page]");
        var action = button.getAttribute("data-v041-ai-action");
        var url = shell ? shell.dataset["ai" + action.charAt(0).toUpperCase() + action.slice(1) + "Url"] : "";
        var originalText = button.textContent;
        button.disabled = true;
        button.textContent = "处理中...";
        requestAi(url, getAiPayload(action, shell)).then(function (data) {
          applyAiResult(action, data.result);
          showMessage("AI 处理完成。");
        }).catch(function (error) {
          showMessage(error.message);
        }).finally(function () {
          button.disabled = false;
          button.textContent = originalText;
        });
      });
    });
  }

  function requestAi(url, payload) {
    if (!url) {
      return Promise.reject(new Error("AI 接口地址缺失。"));
    }
    return fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    }).then(function (response) {
      return response.json().then(function (data) {
        if (!response.ok || !data.ok) {
          throw new Error(data.message || "AI 请求失败。");
        }
        return data;
      });
    });
  }

  function getWriteContent() {
    var title = document.querySelector("[data-v041-write-title]");
    var summary = document.querySelector("[data-v041-write-summary]");
    var content = document.querySelector("[data-v041-write-content]");
    return [
      title && title.value ? "标题：" + title.value.trim() : "",
      summary && summary.value ? "摘要：" + summary.value.trim() : "",
      content && content.value ? "正文：\n" + content.value.trim() : ""
    ].filter(Boolean).join("\n\n");
  }

  function getAiPayload(action, shell) {
    var title = document.querySelector("[data-v041-write-title]");
    var summary = document.querySelector("[data-v041-write-summary]");
    var content = document.querySelector("[data-v041-write-content]");
    var titleText = title && title.value ? title.value.trim() : "";
    var summaryText = summary && summary.value ? summary.value.trim() : "";
    var contentText = content && content.value ? content.value.trim() : "";
    var payload = {
      title: titleText,
      summary: summaryText,
      content: action === "research" ? (titleText || contentText || summaryText) : contentText,
      article_id: shell ? shell.dataset.aiArticleId : ""
    };
    if (action === "research") {
      payload.query = titleText || summaryText || contentText;
    }
    return payload;
  }

  function applyAiResult(action, result) {
    if (action === "summary") {
      var summary = document.querySelector("[data-v041-write-summary]");
      if (summary) {
        summary.value = String(result).slice(0, 500);
        summary.dispatchEvent(new Event("input", { bubbles: true }));
      }
      appendAiMessage("已生成摘要");
      return;
    }
    if (action === "searchSummary") {
      var summary = document.querySelector("[data-v041-write-summary]");
      if (summary) {
        summary.value = String(result).slice(0, 500);
        summary.dispatchEvent(new Event("input", { bubbles: true }));
      }
      appendAiMessage("搜索摘要已生成。发布后系统会继续刷新文章的搜索摘要。");
      return;
    }
    if (action === "research") {
      appendAiMessage("资料搜索结果：\n" + String(result));
      return;
    }
    if (action === "polish") {
      var content = document.querySelector("[data-v041-write-content]");
      if (content) {
        content.value = String(result).replace(/^正文：\s*/, "");
        content.dispatchEvent(new Event("input", { bubbles: true }));
      }
      appendAiMessage("正文已润色，请检查修改效果。");
      return;
    }
    if (action === "tags") {
      applyAiTags(Array.isArray(result) ? result : []);
      return;
    }
    if (action === "outline") {
      appendAiMessage("文章大纲：\n" + String(result));
      return;
    }
    if (action === "title") {
      appendAiMessage("标题建议：\n" + String(result));
      return;
    }
  }

  function applyAiTags(tags) {
    var normalized = tags.map(function (tag) {
      return String(tag).trim().toLowerCase();
    }).filter(Boolean);
    document.querySelectorAll(".write-tag").forEach(function (label) {
      var input = label.querySelector("input[type='checkbox']");
      var text = label.textContent.trim().toLowerCase();
      if (input && normalized.indexOf(text) !== -1) {
        input.checked = true;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      }
    });
    if (normalized.length) {
      appendAiMessage("推荐标签：" + tags.join("、"));
    }
  }

  function appendAiMessage(text) {
    var messages = document.querySelector("[data-v041-ai-messages]");
    if (!messages) {
      return;
    }
    var aiMessage = document.createElement("div");
    aiMessage.className = "write-ai-message is-ai";
    aiMessage.textContent = text;
    messages.appendChild(aiMessage);
    messages.scrollTop = messages.scrollHeight;
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFlashAutoDismiss();
    initConfirmDialog();
    initSearchForms();
    initAiSearch();
    initAuthForms();
    initAiPlaceholders();
    initBackToSearch();
    initPasswordModal();
    initReadingAssistant();
    initWritePage();
    initWriteAiActions();
    initWriteAiChat();
  });
})();

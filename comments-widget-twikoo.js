(function () {
  "use strict";

  var ROOT_SELECTOR = '[data-comments-widget="root"]';
  var AI_NOTE_EN = "Use @AI in a comment to request an in-thread AI response.";
  var AI_NOTE_ZH = "在评论中写 @AI，可触发线程内 AI 回复。";

  function detectLanguage() {
    var lang = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
    return lang.indexOf("zh") === 0 ? "zh" : "en";
  }

  function normalizePath(pathname) {
    var trimmed = pathname.replace(/\/+$/, "");
    return trimmed || "/";
  }

  function resolveCssHref() {
    var current = document.currentScript;
    if (!current) {
      return "comments-widget.css";
    }
    var explicit = current.getAttribute("data-css-href");
    if (explicit) {
      return explicit;
    }
    try {
      var base = new URL(".", current.src);
      return new URL("comments-widget.css", base).toString();
    } catch (err) {
      return "comments-widget.css";
    }
  }

  function ensureCss() {
    if (document.querySelector('link[data-comments-widget-style="1"]')) {
      return;
    }
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = resolveCssHref();
    link.setAttribute("data-comments-widget-style", "1");
    document.head.appendChild(link);
  }

  function addAiNote(root, lang) {
    if (root.querySelector(".pc-comments-note")) {
      return;
    }
    var note = document.createElement("p");
    note.className = "pc-comments-note";
    note.textContent = lang === "zh" ? AI_NOTE_ZH : AI_NOTE_EN;
    root.appendChild(note);
  }

  function loadTwikooScript(src) {
    return new Promise(function (resolve, reject) {
      if (window.twikoo && typeof window.twikoo.init === "function") {
        resolve(window.twikoo);
        return;
      }
      var existing = document.querySelector('script[data-comments-twikoo-script="1"]');
      if (existing) {
        existing.addEventListener("load", function () {
          resolve(window.twikoo);
        });
        existing.addEventListener("error", function () {
          reject(new Error("twikoo_script_load_failed"));
        });
        return;
      }
      var script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.setAttribute("data-comments-twikoo-script", "1");
      script.onload = function () {
        resolve(window.twikoo);
      };
      script.onerror = function () {
        reject(new Error("twikoo_script_load_failed"));
      };
      document.head.appendChild(script);
    });
  }

  function mountTwikoo(root, lang) {
    var envId = root.getAttribute("data-twikoo-env-id");
    var scriptSrc = root.getAttribute("data-twikoo-script-src");
    var region = root.getAttribute("data-twikoo-region");

    if (!envId || envId.indexOf("__") === 0) {
      root.innerHTML =
        '<p class="pc-comments-note">' +
        (lang === "zh"
          ? "评论组件尚未配置完成：请在安装步骤中填写 Twikoo 环境参数。"
          : "Comments are not configured yet. Fill in Twikoo values during setup.") +
        "</p>";
      return;
    }
    if (!scriptSrc || scriptSrc.indexOf("__") === 0) {
      root.innerHTML =
        '<p class="pc-comments-note">' +
        (lang === "zh"
          ? "Twikoo 脚本地址未配置，请在安装步骤中填写。"
          : "Twikoo script URL is missing. Configure it during setup.") +
        "</p>";
      return;
    }

    var host = root.querySelector('[data-role="thread"]');
    if (!host) {
      host = document.createElement("div");
      host.setAttribute("data-role", "thread");
      root.appendChild(host);
    }
    if (!host.id) {
      host.id = "pc-twikoo-" + Math.random().toString(36).slice(2);
    }
    host.classList.add("pc-twikoo-host");
    if (host.getAttribute("data-mounted") === "1") {
      return;
    }
    host.setAttribute("data-mounted", "1");

    loadTwikooScript(scriptSrc)
      .then(function (twikoo) {
        if (!twikoo || typeof twikoo.init !== "function") {
          throw new Error("twikoo_init_missing");
        }
        var path = normalizePath(window.location.pathname);
        var options = {
          envId: envId,
          el: "#" + host.id,
          path: path,
          lang: lang === "zh" ? "zh-CN" : "en",
        };
        if (region) {
          options.region = region;
        }
        return twikoo.init(options);
      })
      .catch(function () {
        host.innerHTML =
          '<p class="pc-comments-note">' +
          (lang === "zh"
            ? "Twikoo 加载失败，请稍后重试或联系维护者。"
            : "Failed to load Twikoo. Please retry later or contact the site owner.") +
          "</p>";
      });
  }

  function init() {
    var root = document.querySelector(ROOT_SELECTOR);
    if (!root) {
      return;
    }
    var lang = detectLanguage();
    ensureCss();
    addAiNote(root, lang);
    mountTwikoo(root, lang);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();

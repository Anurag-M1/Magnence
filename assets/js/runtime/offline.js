(function () {
  "use strict";

  var HOSTED_ASSET = /https:\/\/framerusercontent\.com\/(?:images|assets)\/([^?\s,"')]+)(\?[^,\s"')]+)?/g;
  var BLOCKED_HOSTS = /https:\/\/(?:events\.framer\.com|api\.framer\.com|www\.framer\.com|framer\.com)\b/g;

  function localAssetPath(filename) {
    var clean = filename.split("/").pop();
    var lower = clean.toLowerCase();

    if (/\.(woff2?|ttf|otf|eot)$/.test(lower)) return "/assets/fonts/" + clean;
    if (/\.(mp4|webm|mov)$/.test(lower)) return "/assets/videos/" + clean;
    return "/assets/images/" + clean;
  }

  function localize(value) {
    if (typeof value !== "string") return value;

    return value
      .replace(HOSTED_ASSET, function (_, filename) {
        return localAssetPath(filename);
      })
      .replace(BLOCKED_HOSTS, "#");
  }

  function patchAttributeWrites() {
    var original = Element.prototype.setAttribute;

    Element.prototype.setAttribute = function (name, value) {
      var key = String(name).toLowerCase();

      if (key === "src" || key === "srcset" || key === "href" || key === "poster") {
        return original.call(this, name, localize(value));
      }

      return original.call(this, name, value);
    };
  }

  function patchUrlProperty(proto, prop) {
    var descriptor = Object.getOwnPropertyDescriptor(proto, prop);

    if (!descriptor || !descriptor.set) return;

    Object.defineProperty(proto, prop, {
      configurable: true,
      enumerable: descriptor.enumerable,
      get: descriptor.get,
      set: function (value) {
        descriptor.set.call(this, localize(value));
      },
    });
  }

  function patchFetch() {
    if (!window.fetch) return;

    var original = window.fetch.bind(window);

    window.fetch = function (input, init) {
      if (typeof input === "string") {
        input = localize(input);
      } else if (input && typeof input.url === "string") {
        var nextUrl = localize(input.url);
        if (nextUrl !== input.url) input = new Request(nextUrl, input);
      }

      if (typeof input === "string" && input === "#") {
        return Promise.reject(new TypeError("Blocked external request in offline build"));
      }

      return original(input, init);
    };
  }


  function removeExportedBadges() {
    var selectors = [
      "#__framer-badge-container",
      "#__framer-badge-container-removed",
      ".__framer-badge",
      "[class*='TLVk2']",
      "[class*='TE6Xr']",
      "a[href*='framer.com']",
      "[data-exported-badge]"
    ];

    selectors.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (node) {
        node.remove();
      });
    });
  }

  function rewriteExistingAttributes() {
    document.querySelectorAll("[src], [srcset], [href], [poster]").forEach(function (node) {
      ["src", "srcset", "href", "poster"].forEach(function (name) {
        if (!node.hasAttribute(name)) return;

        var value = node.getAttribute(name);
        var next = localize(value);
        if (next !== value) node.setAttribute(name, next);
      });
    });
  }

  patchAttributeWrites();
  patchUrlProperty(HTMLImageElement.prototype, "src");
  patchUrlProperty(HTMLScriptElement.prototype, "src");
  patchUrlProperty(HTMLLinkElement.prototype, "href");
  patchUrlProperty(HTMLAnchorElement.prototype, "href");
  patchUrlProperty(HTMLSourceElement.prototype, "src");
  patchFetch();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      rewriteExistingAttributes();
      removeExportedBadges();
    }, { once: true });
  } else {
    rewriteExistingAttributes();
    removeExportedBadges();
  }

  new MutationObserver(removeExportedBadges).observe(document.documentElement, { childList: true, subtree: true });
})();

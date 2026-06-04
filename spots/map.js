/* ============================================================
   UNC Skate Club — spot map (v1, read-only)
   Vanilla JS + Leaflet. Snapshot-first paint, guarded API hydrate.
   ============================================================ */
(function () {
  "use strict";

  // ---- config ----
  var API_BASE = "http://localhost:8000";   // backend dev default; absent in v1 → snapshot stands
  var SNAPSHOT_URL = "data/public-spots.json";
  var HYDRATE_TIMEOUT_MS = 3000;
  var CENTER = [35.911, -79.060];
  var ZOOM = 13;

  var TYPES = ["ledge", "stairs", "rail", "transition", "flat", "DIY"];
  var TYPE_LABELS = {
    ledge: "ledges", stairs: "stairs", rail: "rails",
    transition: "transition", flat: "flat", DIY: "DIY"
  };
  var BUSTS = ["chill", "caution", "hot"];
  var BUST_WORDS = { chill: "nobody cares", caution: "depends on the day", hot: "you'll get kicked" };

  // ---- tiny helpers ----
  function $(sel) { return document.querySelector(sel); }

  // escape any user-originated string before it touches the DOM
  function esc(s) {
    if (s == null) return "";
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  // photo URL allowlist: relative assets/... or https://. Reject everything else.
  function safePhoto(url) {
    if (typeof url !== "string") return null;
    var u = url.trim();
    if (u === "") return null;
    if (/^\/\//.test(u)) return null;                 // protocol-relative
    if (/^https:\/\//i.test(u)) return u;             // https only
    if (/^(\.\.\/)*assets\//.test(u)) return u;       // repo-relative assets path
    return null;                                      // javascript:, data:, http:, etc.
  }

  // "last verified" in skater phrasing, computed from the ISO date
  function verifiedPhrase(spot) {
    if (!spot.verified) return "nobody's checked lately — roll up and see";
    var d = new Date(spot.verified + "T00:00:00");
    if (isNaN(d)) return "nobody's checked lately — roll up and see";
    var mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][d.getMonth()];
    var stamp = mon + " '" + String(d.getFullYear()).slice(2);
    var months = (Date.now() - d.getTime()) / (1000 * 60 * 60 * 24 * 30);
    if (months <= 3) return "last skated " + stamp;
    return "last we checked, " + stamp + " — might've changed";
  }

  // build the marker divIcon HTML. All markers are one Carolina capsule; the glyph
  // is the only differentiator (= obstacle type). bust lives in the filter + popup.
  // type drives an SVG <use href="#g-..."> ref, so validate it against the known
  // vocabulary — untrusted data (v2 submissions) must not break out. Unknown → no glyph.
  function markerHTML(spot) {
    var type = TYPES.indexOf(spot.type) >= 0 ? spot.type : null;
    var glyph = type
      ? '<svg class="cap__glyph" viewBox="0 0 24 24" aria-hidden="true"><use href="#g-' +
        type + '"></use></svg>'
      : "";
    var tick = (spot.clips && spot.clips.length) || (spot.videos && spot.videos.length)
      ? '<span class="cap__tick" aria-hidden="true"></span>' : "";
    return '<span class="cap">' + glyph + tick + '</span><span class="cap__notch"></span>';
  }

  // ---- map setup ----
  var map = L.map("map", { zoomControl: false, attributionControl: true })
    .setView(CENTER, ZOOM);

  L.control.zoom({ position: "bottomright" }).addTo(map);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  // state
  var allSpots = [];
  var markers = [];                       // { marker, spot }
  var activeTypes = {};                    // type -> bool (empty = all)
  var activeBusts = {};                    // bust -> bool (empty = all)

  // ---- markers ----
  function makeIcon(spot) {
    return L.divIcon({
      className: "spot-pin",
      html: markerHTML(spot),
      iconSize: [44, 44],
      iconAnchor: [22, 40]               // notch points at the coordinate
    });
  }

  function renderMarkers() {
    markers.forEach(function (m) { map.removeLayer(m.marker); });
    markers = [];
    allSpots.forEach(function (spot) {
      if (typeof spot.lat !== "number" || typeof spot.lng !== "number") return;
      var marker = L.marker([spot.lat, spot.lng], { icon: makeIcon(spot) });
      marker.on("click", function () { openSheet(spot); });
      markers.push({ marker: marker, spot: spot });
    });
    applyFilters();
  }

  // ---- filtering ----
  function passesFilter(spot) {
    var typeKeys = Object.keys(activeTypes);
    var bustKeys = Object.keys(activeBusts);
    if (typeKeys.length && !activeTypes[spot.type]) return false;
    if (bustKeys.length && !activeBusts[spot.bust]) return false;
    return true;
  }

  function applyFilters() {
    var shown = 0;
    markers.forEach(function (m) {
      if (passesFilter(m.spot)) {
        if (!map.hasLayer(m.marker)) m.marker.addTo(map);
        shown++;
      } else if (map.hasLayer(m.marker)) {
        map.removeLayer(m.marker);
      }
    });
    var emptyNote = $("#emptyNote");
    if (shown === 0 && markers.length > 0) emptyNote.hidden = false;
    else emptyNote.hidden = true;
  }

  // ---- chips ----
  function makeChip(label, kind, value) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "chip chip--" + kind + (kind === "bust" ? " chip--bust-" + value : "");
    if (kind === "type") {
      btn.innerHTML = '<svg class="chip__glyph" viewBox="0 0 24 24" aria-hidden="true">' +
        '<use href="#g-' + value + '"></use></svg>' +
        '<span class="chip__label"></span>';
      btn.querySelector(".chip__label").textContent = label;   // label is from our constant, still set safely
    } else {
      btn.textContent = label;
    }
    btn.addEventListener("click", function () {
      var set = kind === "type" ? activeTypes : activeBusts;
      if (set[value]) { delete set[value]; btn.classList.remove("is-active"); }
      else { set[value] = true; btn.classList.add("is-active"); }
      applyFilters();
    });
    return btn;
  }

  function buildChips() {
    var typeRow = $("#typeRow");
    TYPES.forEach(function (t) { typeRow.appendChild(makeChip(TYPE_LABELS[t], "type", t)); });
    var bustRow = $("#bustRow");
    BUSTS.forEach(function (b) { bustRow.appendChild(makeChip(b, "bust", b)); });

    $("#resetChip").addEventListener("click", function () {
      activeTypes = {}; activeBusts = {};
      document.querySelectorAll(".chip.is-active").forEach(function (c) { c.classList.remove("is-active"); });
      applyFilters();
    });
  }

  // ---- detail sheet ----
  function openSheet(spot) {
    var body = $("#sheetBody");
    var html = "";

    // name (Anton)
    html += '<h2 class="sheet__name">' + esc(spot.name) + "</h2>";

    // type + bust capsule tags + plain-words bust
    html += '<div class="sheet__tags">';
    html += '<span class="tag tag--type"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#g-' +
      esc(spot.type) + '"></use></svg>' + esc(TYPE_LABELS[spot.type] || spot.type) + "</span>";
    if (spot.bust) {
      html += '<span class="tag tag--bust tag--bust-' + esc(spot.bust) + '">' + esc(spot.bust) + "</span>";
    }
    html += "</div>";
    if (spot.bust && BUST_WORDS[spot.bust]) {
      html += '<p class="sheet__bustword">' + esc(BUST_WORDS[spot.bust]) + "</p>";
    }

    // lead photo: reserve a wrapper here; the sanitized <img> is injected via DOM below
    var photoSrc = (spot.photos && spot.photos.length) ? safePhoto(spot.photos[0]) : null;
    if (photoSrc) html += '<div class="sheet__photo-wrap" data-photo="1"></div>';

    // facts line (Special Elite): surface · size · area — skip empties
    var facts = [spot.surface, spot.size, spot.area].filter(Boolean).map(esc);
    if (facts.length) html += '<p class="sheet__facts">' + facts.join(" · ") + "</p>";

    // notes
    if (spot.notes) html += '<p class="sheet__notes">' + esc(spot.notes) + "</p>";

    // clips: magenta tick row when present (no embeds in v1)
    var clipCount = (spot.clips && spot.clips.length) || (spot.videos && spot.videos.length) || 0;
    if (clipCount) html += '<p class="sheet__clips">▸ clips (' + esc(clipCount) + ")</p>";

    // last verified (Special Elite, muted)
    html += '<p class="sheet__verified">' + esc(verifiedPhrase(spot)) + "</p>";

    body.innerHTML = html;

    // inject the sanitized photo node (kept out of the innerHTML string for safety)
    if (photoSrc) {
      var wrap = body.querySelector('[data-photo="1"]');
      if (wrap) {
        var photo = document.createElement("img");
        photo.className = "sheet__photo";
        photo.loading = "lazy";
        photo.alt = spot.name || "";        // textContent-equivalent; .src/.alt set as properties, not parsed as HTML
        photo.src = photoSrc;
        wrap.appendChild(photo);
      }
    }

    var sheet = $("#detailSheet");
    sheet.hidden = false;
    sheet.setAttribute("aria-hidden", "false");
  }

  function closeSheet() {
    var sheet = $("#detailSheet");
    sheet.hidden = true;
    sheet.setAttribute("aria-hidden", "true");
  }

  // ---- data loading: snapshot-first, guarded hydrate ----
  function normalize(raw) {
    // accept either the snapshot shape { spots: [...] } or a bare array (API)
    if (Array.isArray(raw)) return raw;
    if (raw && Array.isArray(raw.spots)) return raw.spots;
    return [];
  }

  function loadSnapshot() {
    return fetch(SNAPSHOT_URL).then(function (r) {
      if (!r.ok) throw new Error("snapshot " + r.status);
      return r.json();
    }).then(normalize);
  }

  function hydrate() {
    if (!("AbortController" in window)) return Promise.reject();
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, HYDRATE_TIMEOUT_MS);
    return fetch(API_BASE + "/api/spots", { signal: ctrl.signal })
      .then(function (r) { clearTimeout(t); if (!r.ok) throw new Error("api " + r.status); return r.json(); })
      .then(normalize);
  }

  function paint(spots) {
    allSpots = spots;
    renderMarkers();
    var stamp = $("#loadStamp");
    if (stamp) stamp.remove();
  }

  // ---- boot ----
  buildChips();

  $("#sheetClose").addEventListener("click", closeSheet);
  map.on("click", closeSheet);   // tap the map to dismiss the sheet

  loadSnapshot().then(function (snapshot) {
    paint(snapshot);
    // try to hydrate from the live API; keep snapshot silently if it fails
    hydrate().then(function (fresh) {
      if (fresh && fresh.length) paint(fresh);
    }).catch(function () {
      // an API hydrate was ATTEMPTED and FAILED → show the masking-tape banner
      var banner = $("#staleBanner");
      if (banner) banner.hidden = false;
    });
  }).catch(function () {
    // even the snapshot failed — honest, no spinner-of-doom
    var stamp = $("#loadStamp");
    if (stamp) {
      stamp.querySelector("span").textContent = "map's down right now — hit us on IG";
    }
  });
})();

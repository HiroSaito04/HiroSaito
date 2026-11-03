(function (root) {
  "use strict";
  const FONT = {
    A: ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    B: ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    C: ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    D: ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    E: ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    F: ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    G: ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    H: ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    I: ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    J: ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    K: ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    L: ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    M: ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    N: ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    O: ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    P: ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    Q: ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    R: ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    S: ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    T: ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    U: ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    V: ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    W: ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    X: ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    Y: ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    Z: ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    0: ["01110", "10011", "10101", "10101", "11001", "10001", "01110"],
    1: ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    2: ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    3: ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    4: ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    5: ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    6: ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    7: ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    8: ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    9: ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00100", "00100"],
    ":": ["00000", "00100", "00100", "00000", "00100", "00100", "00000"],
    "/": ["00001", "00001", "00010", "00100", "01000", "10000", "10000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    _: ["00000", "00000", "00000", "00000", "00000", "00000", "11111"],
    ">": ["10000", "01000", "00100", "00010", "00100", "01000", "10000"],
    "<": ["00001", "00010", "00100", "01000", "00100", "00010", "00001"],
    "@": ["01110", "10001", "10111", "10101", "10111", "10000", "01111"],
    "#": ["01010", "11111", "01010", "11111", "01010", "00000", "00000"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "!": ["00100", "00100", "00100", "00100", "00000", "00100", "00000"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    "|": ["00100", "00100", "00100", "00100", "00100", "00100", "00100"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "•": ["00000", "00000", "01110", "01110", "01110", "00000", "00000"],
    "(": ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ")": ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
  };
  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function clamp(v, a, b) {
    return Math.max(a, Math.min(b, v));
  }
  function safeHex(v, fallback) {
    return /^#[0-9a-fA-F]{6}$/.test(v || "") ? v : fallback;
  }
  function bitmap(text, x, y, scale, color, maxWidth) {
    let content = String(text || "").toUpperCase();
    let spacing = 1,
      unitW = 6;
    const rawWidth = Math.max(0, content.length * unitW - 1);
    const fittedScale = maxWidth
      ? Math.min(scale, maxWidth / Math.max(1, rawWidth))
      : scale;
    // pixel blocks stay crisp, even when a long editable string needs to fit
    let parts = [];
    let cx = 0;
    for (const char of content) {
      const g = FONT[char] || FONT["?"];
      for (let r = 0; r < 7; r++)
        for (let col = 0; col < 5; col++) {
          if (g[r][col] === "1") {
            let xx = x + (cx + col) * fittedScale,
              yy = y + r * fittedScale;
            parts.push(
              `M${xx.toFixed(2)} ${yy.toFixed(2)}h${fittedScale.toFixed(2)}v${fittedScale.toFixed(2)}h-${fittedScale.toFixed(2)}z`,
            );
          }
        }
      cx += 6;
    }
    return `<g fill="${color}" shape-rendering="crispEdges" aria-label="${esc(text)}"><path d="${parts.join("")}"/></g>`;
  }
  function pixelForest() {
    let s = "";
    // bottom pixel-grass texture and pine silhouettes
    for (let x = 745; x < 1370; x += 18) {
      const v = 27 + Math.round((Math.sin(x * 0.041) + 1) * 13);
      s += `<rect x="${x}" y="${516 - v}" width="16" height="${v}" fill="#234325" opacity=".66"/>`;
    }
    const trees = [
      [1000, 48],
      [1108, 78],
      [1230, 112],
      [1315, 70],
    ];
    for (const [x, h] of trees) {
      s += `<rect x="${x - 6}" y="${515 - h / 3}" width="12" height="${h / 3}" fill="#315e2d"/>`;
      for (let i = 0; i < 5; i++) {
        const w = (i + 1) * h * 0.19,
          yy = 515 - h + (i + 1) * h * 0.15;
        s += `<rect x="${(x - w / 2).toFixed(0)}" y="${yy.toFixed(0)}" width="${w.toFixed(0)}" height="${(h * 0.16).toFixed(0)}" fill="#315f2f"/>`;
      }
    }
    return s;
  }
  function chamferPath(x, y, w, h, c = 17) {
    return `M${x + c} ${y}H${x + w - c}L${x + w} ${y + c}V${y + h - c}L${x + w - c} ${y + h}H${x + c}L${x} ${y + h - c}V${y + c}Z`;
  }
  function box(x, y, w, h, c, fill, stroke, width = 4) {
    return `<path d="${chamferPath(x, y, w, h, c)}" fill="${fill}" stroke="${stroke}" stroke-width="${width}" stroke-linejoin="miter"/>`;
  }
  function cross(x, y, sz, col) {
    return `<path d="M${x - sz / 4} ${y - sz}h${sz / 2}v${sz * 0.75}h${sz * 0.75}v${sz / 2}h-${sz * 0.75}v${sz * 0.75}h-${sz / 2}v-${sz * 0.75}h-${sz * 0.75}v-${sz / 2}h${sz * 0.75}z" fill="${col}"/>`;
  }
  function renderCard(config, avatarDataUri) {
    let accent = safeHex(config.accent, "#8bdd54");
    const title = String(config.displayName || "MR. ZHIROARK");
    const handle = String(config.username || "HiroSaito04");
    const role = String(config.role || "DEVELOPER • CREATIVE CODER");
    const tagline = String(
      config.tagline || "Building thoughtful digital experiences.",
    );
    const gh = String(config.githubLabel || "github.com/HiroSaito04");
    let avatar = "";
    if (
      /^data:image\/(png|jpeg|jpg|webp);base64,[A-Za-z0-9+/=]+$/.test(
        avatarDataUri || "",
      )
    ) {
      avatar = `<image x="143" y="158" width="252" height="294" href="${avatarDataUri}" preserveAspectRatio="xMidYMid meet" style="image-rendering:pixelated" clip-path="url(#avatarClip)"/>`;
    }
    let s = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1400" height="600" viewBox="0 0 1400 600" role="img" aria-label="Pixel profile card for ${esc(title)}">
<title>${esc(title)} — Pixel developer profile card</title><desc>Editable, fully code-drawn retro game profile card for ${esc(handle)}.</desc><metadata id="pixelCardEditorState">${esc(JSON.stringify({ config, avatarDataUri }))}</metadata>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101818"/><stop offset="1" stop-color="#0b1510"/></linearGradient>
  <linearGradient id="avatarBg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#244522"/><stop offset="1" stop-color="#385e2b"/></linearGradient>
  <clipPath id="avatarClip"><rect x="129" y="139" width="278" height="333"/></clipPath>
</defs>
<rect width="1400" height="600" fill="#0b1111"/>
<rect x="25" y="30" width="1350" height="530" fill="url(#bg)"/>
${box(53, 58, 1294, 470, 31, "#111c17", accent, 5)}
<path d="M83 70H1315" stroke="#345530" stroke-width="2"/>
${pixelForest()}
${box(108, 132, 326, 343, 40, "url(#avatarBg)", accent, 6)}
${box(119, 142, 304, 322, 33, "#30542b", "#467f35", 2)}
${avatar}
${box(489, 130, 338, 58, 15, "#0c1813", "#477b36", 4)}
${bitmap(">_ " + handle, 512, 148, 4.7, "#f2f7eb", 292)}
${bitmap(title, 490, 222, 8.4, "#f8f8ed", 796)}
${bitmap(role, 495, 313, 4.7, accent, 805)}
<rect x="495" y="376" width="768" height="8" fill="#234022"/>
<rect x="495" y="376" width="150" height="8" fill="${accent}"/>
${bitmap(tagline, 495, 409, 3.3, "#c2cdc4", 770)}
${box(489, 457, 620, 53, 15, "#0b1812", "#4e843c", 4)}
${bitmap(">_", 515, 472, 3.7, accent, 46)}
${bitmap(gh, 590, 472, 3.5, "#f5f7ed", 490)}
${cross(1245, 223, 18, accent)}
${cross(1296, 421, 12, accent)}
<rect x="1249" y="112" width="17" height="17" fill="#244326"/>
<rect x="1266" y="129" width="17" height="17" fill="#244326"/>
<rect x="1283" y="112" width="17" height="17" fill="#244326"/>
<rect x="1283" y="146" width="17" height="17" fill="#244326"/>
</svg>`;
    return s;
  }
  const api = { renderCard, bitmap, FONT };
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.PixelCard = api;
})(typeof window !== "undefined" ? window : globalThis);

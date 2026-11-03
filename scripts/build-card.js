/* Zero-dependency build: node scripts/build-card.js */
const fs = require("node:fs");
const path = require("node:path");
const { renderCard } = require("./card-renderer.js");
const root = path.resolve(__dirname, "..");
const config = JSON.parse(fs.readFileSync(path.join(root, "profile.json"), "utf8"));
const imagePath = path.resolve(root, config.avatar || "assets/boy_down.png");
if (!imagePath.startsWith(root + path.sep)) {
  throw new Error("Avatar path must be inside the project folder.");
}
const ext = path.extname(imagePath).toLowerCase();
const mime = {
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
}[ext];
if (!mime) throw new Error("Avatar must be PNG, JPG or WebP.");
const dataUrl = `data:${mime};base64,${fs.readFileSync(imagePath).toString("base64")}`;
const svg = renderCard(config, dataUrl);
fs.writeFileSync(path.join(root, "assets", "profile-card.svg"), svg, "utf8");
// Updated offline editor defaults, so editing profile.json + rebuild refreshes editor.html.
fs.writeFileSync(
  path.join(root, "scripts", "default-config.js"),
  `window.DEFAULT_PIXEL_CARD=${JSON.stringify(config, null, 2)};\nwindow.DEFAULT_AVATAR_DATA=${JSON.stringify(dataUrl)};\n`,
  "utf8",
);
console.log("Generated assets/profile-card.svg and refreshed editor defaults.");

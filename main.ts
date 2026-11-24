// news-image-20261124: write the one-page world-news image to /output/entry.png.
//
// The image is entry.png in this repository (drawn with code by render.py:
// a front page summing up Tuesday 24 November 2026 — COP31 collapses in
// Antalya, Nvidia's Huang returns as the US blacklists Megaspeed, Zelensky
// urges four-party talks, 24 dead in an Indonesia factory fire, and a Japan
// trade deal). This program copies it byte for byte, so two runs write
// identical bytes. No network, no randomness, Node 22 standard library only.
import { chmodSync, copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const src = join(root, "entry.png");
const outDir = "/output";
mkdirSync(outDir, { recursive: true });
const out = join(outDir, "entry.png");
copyFileSync(src, out);
chmodSync(out, 0o644);
console.log("wrote /output/entry.png");

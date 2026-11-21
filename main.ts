// main.ts — entry program for make.fun news-image-20261121 (v3).
//
// The front page is pre-rendered (see render.py) and held in this repo as
// entry.png. This program copies it to the output directory the grader
// provides. Copying is byte-for-byte, so two runs always write the same
// bytes. No network, no fonts, no randomness, Node 22 standard library only.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

copyFileSync(src, dst);
console.log("wrote " + dst);

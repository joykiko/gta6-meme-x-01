// Copy the post reference into the grading output directory.
// The image and post text are the entry; this program only hands over POST.json.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const repository = process.env.MAKEFUN_BOT_DIR || '/bot';
const destination = process.env.MAKEFUN_OUTPUT_DIR || '/output';

mkdirSync(destination, { recursive: true });

try {
  copyFileSync(join(repository, 'POST.json'), join(destination, 'POST.json'));
} catch (error) {
  const details = error instanceof Error ? error.message : String(error);
  console.error(`Could not copy POST.json from ${repository}: ${details}`);
  process.exitCode = 1;
}

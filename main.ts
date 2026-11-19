// Copy the post reference into the grading output directory.
// The image and post text are the entry; this program only hands over POST.json.

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const repository = process.env.MAKEFUN_BOT_DIR || '/bot';
const destination = process.env.MAKEFUN_OUTPUT_DIR || '/output';

try {
  const source = join(repository, 'POST.json');
  const post: unknown = JSON.parse(readFileSync(source, 'utf8'));
  if (
    post === null || typeof post !== 'object' || Array.isArray(post) ||
    !('url' in post) || typeof post.url !== 'string' || post.url.trim().length === 0
  ) {
    throw new Error('POST.json must be a JSON object with a non-empty string "url"');
  }

  // Validate first, then preserve the source bytes exactly for the handoff.
  mkdirSync(destination, { recursive: true });
  copyFileSync(source, join(destination, 'POST.json'));
} catch (error) {
  const details = error instanceof Error ? error.message : String(error);
  console.error(`Could not validate or copy POST.json from ${repository}: ${details}`);
  process.exitCode = 1;
}

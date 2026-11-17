import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const CHECKER = fileURLToPath(import.meta.url);
const SKIP_DIRECTORIES = new Set([
  ".git",
  "__pycache__",
  "node_modules",
  "output",
  "screenshots",
  "tmp",
]);
const TEXT_EXTENSIONS = new Set([
  ".css",
  ".html",
  ".js",
  ".json",
  ".md",
  ".mjs",
  ".ps1",
  ".py",
  ".srt",
  ".txt",
  ".yaml",
  ".yml",
]);

async function collectFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    if (entry.isDirectory() && SKIP_DIRECTORIES.has(entry.name)) {
      continue;
    }

    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await collectFiles(fullPath)));
      continue;
    }

    if (TEXT_EXTENSIONS.has(path.extname(entry.name).toLowerCase())) {
      files.push(fullPath);
    }
  }

  return files;
}

const files = await collectFiles(ROOT);
const problems = [];

for (const file of files) {
  const relativePath = path.relative(ROOT, file);
  const content = await readFile(file, "utf8");
  const lines = content.split(/\r?\n/);

  if (content.includes("\r")) {
    problems.push(`${relativePath}: use LF line endings`);
  }

  lines.forEach((line, index) => {
    const lineNumber = index + 1;
    if (line.includes("\t")) {
      problems.push(`${relativePath}:${lineNumber}: tab character`);
    }
    if (/[ \t]+$/.test(line)) {
      problems.push(`${relativePath}:${lineNumber}: trailing whitespace`);
    }
    if (
      file !== CHECKER &&
      [".js", ".mjs"].includes(path.extname(file)) &&
      /\bdebugger\b/.test(line)
    ) {
      problems.push(`${relativePath}:${lineNumber}: debugger statement`);
    }
  });

  if (content.length > 0 && !content.endsWith("\n")) {
    problems.push(`${relativePath}: missing final newline`);
  }
  if (content.endsWith("\n\n")) {
    problems.push(`${relativePath}: extra blank line at end of file`);
  }
}

if (problems.length > 0) {
  console.error(`Code style check failed with ${problems.length} issue(s):`);
  for (const problem of problems.slice(0, 100)) {
    console.error(`- ${problem}`);
  }
  process.exitCode = 1;
} else {
  console.log(`Code style check passed (${files.length} files).`);
}

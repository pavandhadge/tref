---
library: npm
version: "9.8.0"
category: api
item: npm.install
type: command
signature: "npm install <package> [--save|--save-dev|--save-optional]"
keywords: ["install", "add", "package", "dependency"]
aliases: ["npm i", "install package", "add dependency"]
intent: "Install a package and its dependencies from npm registry, adding them to package.json."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://docs.npmjs.com/cli/v9/commands/npm-install"
source_title: "npm install Documentation"
alternatives:
  - option: "yarn add"
    reason: "Faster, offline cache, deterministic installs."
  - option: "pnpm add"
    reason: "Disk efficient, strict dependency management."
  - option: "uv pip install"
    reason: "For Python packages, not JavaScript."
---

# npm install

## Signature
```bash
npm install <package>
npm install <package>@<version>
npm install <package> --save-dev
npm install <package> --save-optional
npm install
```

## What It Does
Installs packages from npm registry. For local projects, adds to `node_modules` and records in `package.json`. Without arguments, installs all dependencies from package.json.

## Use When
- Adding packages to your project.
- Installing project dependencies from package.json.
- Installing development tools (testing, linting).
- Installing packages globally (npm install -g).

## Examples
```bash
npm install lodash
```

```bash
npm install express --save
```

```bash
npm install jest --save-dev
```

```bash
npm install @types/node --save-dev
```

```bash
npm install
```

```bash
npm install lodash@4.17.21
```

```bash
npm install lodash@latest
```

```bash
npm install
```

## Returns
Packages installed in node_modules

## Gotchas / Version Notes
- `--save` is default (records in dependencies).
- `--save-dev` or `-D` for devDependencies.
- `--save-optional` or `-O` for optionalDependencies.
- Use `--legacy-peer-deps` for older package compatibility.
- Use `npm ci` for CI/CD (faster, clean install).

## References
- npm install: https://docs.npmjs.com/cli/v9/commands/npm-install
- package.json: https://docs.npmjs.com/cli/v9/configuring-npm/package-json

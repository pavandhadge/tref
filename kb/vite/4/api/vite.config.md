---
library: vite
version: "4.5.0"
category: api
item: vite.config
type: config
signature: "export default defineConfig({ plugins: [], build: {} })"
keywords: ["vite", "config", "build", "plugin"]
aliases: ["vite config", "vite.config.js", "configuration"]
intent: "Configure Vite build tool with plugins, build options, server settings, and optimization settings."
last_updated: "2025-03-02"
schema_version: "2.0"
source_url: "https://vitejs.dev/config/"
source_title: "Vite Configuration Documentation"
alternatives:
  - option: "webpack"
    reason: "More mature but slower, requires more config."
  - option: "Rollup"
    reason: "Underlying bundler for Vite, used directly for libraries."
  - option: "Parcel"
    reason: "Zero-config bundler, less flexible."
---

# Vite Config

## Signature
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
  build: { outDir: 'dist' },
});
```

## What It Does
Configures Vite's dev server, build options, plugins, and environment variables. Supports ES modules config file (vite.config.js/ts/mjs). Uses native ES modules.

## Use When
- Setting up build output directories.
- Adding framework plugins (React, Vue, Svelte).
- Configuring dev server proxy.
- Setting environment variables.

## Examples
```javascript
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:5000',
    },
  },
});
```

```javascript
export default defineConfig({
  build: {
    outDir: 'build',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
});
```

```javascript
export default defineConfig({
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
```

```javascript
export default defineConfig(({ mode }) => ({
  define: {
    'process.env.NODE_ENV': JSON.stringify(mode),
  },
}));
```

## Returns
Configuration object

## Gotchas / Version Notes
- Use `defineConfig` for TypeScript support and IDE hints.
- Plugin order matters in some cases.
- Use `envPrefix` to avoid env variable conflicts.
- SSR has separate config with ssr: true option.
- Works with .env files for environment variables.

## References
- Vite config: https://vitejs.dev/config/
- Plugins: https://vitejs.dev/plugins/

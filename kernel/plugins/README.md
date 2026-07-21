# CAMEAL Kernel Plugin Framework

This directory contains the **infrastructure** for loading and managing plugins.

It provides:
- Plugin manifest parsing (`manifest.yaml`)
- Plugin discovery and loading
- Plugin registration with the kernel
- Plugin lifecycle hooks

**Important:** This is the *framework* for plugins, not the plugins themselves.

Domain plugins (RAG, ML, Governance, etc.) should be developed as separate Python packages that depend on this framework and the kernel.

They should be placed in the plugin search path (e.g., `plugins/` at the project root), not inside `kernel/plugins/`.

---

**Related:** `kernel/EXTENSION_GUIDE.md` – how to create a plugin.

import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: {
    // Listen on all interfaces so the browser on your machine can reach the container.
    host: true,
    port: 5173,
    strictPort: true,
    // Forward /api to the backend container, mirroring what nginx does when deployed.
    // Code always calls relative URLs like /api/v1/notes.
    proxy: {
      "/api": "http://backend:8000",
    },
  },
});

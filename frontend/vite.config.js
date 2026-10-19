import { defineConfig } from "vite";

export default defineConfig({
  server: {
    // Požadavky na /api přeposílej na backend
    proxy: {
      "/api": "http://localhost:8000",
    },
  },
});
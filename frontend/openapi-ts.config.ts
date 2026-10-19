import { defineConfig } from "@hey-api/openapi-ts";

// Generates a typed client from the backend's contract. Run `mise run client:generate`.
export default defineConfig({
  input: "../backend/openapi.json",
  output: "src/client",
  plugins: ["@hey-api/client-fetch"],
});

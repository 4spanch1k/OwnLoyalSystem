import { defineConfig, loadEnv } from "vite";
import path from "path";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const loyaltyProxyTarget = env.VITE_LOYALTY_PROXY_TARGET || "http://127.0.0.1:8000";

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      proxy: {
        "/api": {
          target: loyaltyProxyTarget,
          changeOrigin: true,
        },
      },
    },
    assetsInclude: ["**/*.svg", "**/*.csv"],
  };
});

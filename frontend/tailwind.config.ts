import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        ink: "#111827",
        paper: "#f6f2e8",
        signal: "#d97706",
        moss: "#2f5d50"
      }
    }
  },
  plugins: []
};

export default config;

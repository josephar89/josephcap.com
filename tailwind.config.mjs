import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', '"Noto Sans Tamil"', "system-ui", "sans-serif"],
        serif: ['"Merriweather"', '"Noto Serif Tamil"', "Georgia", "serif"],
      },
    },
  },
  plugins: [typography],
};

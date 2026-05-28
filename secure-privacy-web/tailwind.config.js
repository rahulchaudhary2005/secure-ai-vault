/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00F5D4',
        secondary: '#7B2CBF',
        dark: '#050816',
      },

      boxShadow: {
        neon: '0 0 20px rgba(0,245,212,0.4)',
      },
    },
  },
  plugins: [],
}
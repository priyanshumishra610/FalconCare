/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s infinite',
        'ping-slow': 'ping 3s infinite',
      },
      colors: {
        'falcon-blue': '#1e90ff',
        'falcon-green': '#4ecdc4',
        'falcon-purple': '#45b7d1',
      }
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'jump': 'jump 1.4s infinite ease-in-out both',
        'jump-delay-1': 'jump 1.4s infinite ease-in-out both 0.2s',
        'jump-delay-2': 'jump 1.4s infinite ease-in-out both 0.4s',
      },
      keyframes: {
        jump: {
          '0%, 80%, 100%': { transform: 'scale(0)' },
          '40%': { transform: 'scale(1.0)' },
        },
      },
    },
  },
  plugins: [
  ],
}
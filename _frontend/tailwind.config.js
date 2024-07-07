/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    './src/**/*.{html,js}',
  ],
  theme: {
    extend: {
      boxShadow: {
        gold: '0px 0px 20px 2px rgba(255,215,0,1)',
      },
      colors: {
        gold: '#FFD700',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

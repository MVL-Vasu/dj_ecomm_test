/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './ecommerce/**/*.{html,js,py}',
    './products/**/*.{html,js,py}',
    './cart/**/*.{html,js,py}',
    './orders/**/*.{html,js,py}',
    './accounts/**/*.{html,js,py}',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
}

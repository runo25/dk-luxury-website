/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Scan all .html files in the templates directory and subdirectories
    './**/forms.py', // Scan form widgets if they add classes
    // Add any other paths where Tailwind classes might be used
  ],
  theme: {
    extend: {
      // You can add custom colors, fonts, etc. here later if needed
      // Example from your prompt:
      colors: {
        'dk-pink': '#FADADD', // Example soft pink
        'dk-gold': '#E1C48F', // Example muted gold
        'dk-offwhite': '#FAF8F7', // Example off-white
      },
      fontFamily: {
        // Ensure these fonts are linked via Google Fonts in your HTML
        'serif': ['Cormorant Garamond', 'serif'],
        'sans': ['Lato', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

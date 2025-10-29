/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#4C51BF",
        accent: "#F6AD55",
        danger: "#E53E3E",
        success: "#38A169",
        background: "#EDF2F7"
      }
    }
  },
  plugins: []
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/**/*.html",
    "./app_main/templates/**/*.html",
    "./app_users/templates/**/*.html",
    "./content/templates/**/*.html",
    "./assets/js/**/*.js",
  ],
  theme: {
    extend: {
      // Semantic tokens map to CSS variables that flip in dark mode,
      // so `bg-paper` / `text-ink` etc. are theme-aware with no dark: variant.
      colors: {
        paper: "var(--paper)",
        paper2: "var(--paper-2)",
        paper3: "var(--paper-3)",
        ink: "var(--ink)",
        ink2: "var(--ink-2)",
        ink3: "var(--ink-3)",
        line: "var(--line)",
        line2: "var(--line-2)",
        accent: "var(--accent)",
        accent2: "var(--accent-2)",
        accentSoft: "var(--accent-soft)",
        accentInk: "var(--accent-ink)",
        amber: "var(--amber)",
        amberSoft: "var(--amber-soft)",
      },
      fontFamily: {
        serif: ['Newsreader', 'Georgia', 'Cambria', 'serif'],
        sans: ['Inter', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      maxWidth: {
        content: "1120px",
        prose2: "720px",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(20,23,28,.04), 0 8px 30px rgba(20,23,28,.06)",
        lift: "0 1px 2px rgba(20,23,28,.05), 0 20px 50px rgba(20,23,28,.10)",
      },
    },
  },
  plugins: [],
};

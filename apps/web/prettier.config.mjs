/** Mirrors the extension's style: no semicolons, single quotes. */
export default {
  semi: false,
  singleQuote: true,
  trailingComma: 'none',
  plugins: [
    'prettier-plugin-organize-imports',
    'prettier-plugin-astro',
    'prettier-plugin-tailwindcss'
  ],
  overrides: [
    {
      files: '*.astro',
      options: { parser: 'astro' }
    }
  ]
}

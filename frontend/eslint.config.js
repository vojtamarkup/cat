import js from "@eslint/js";
import globals from "globals";

export default [
  // Složku s buildem nekontroluj
  { ignores: ["dist"] },

  // Doporučená pravidla (nepoužité proměnné, překlepy apod.)
  js.configs.recommended,

  // Kód běží v prohlížeči, takže document, fetch apod. existují
  { languageOptions: { globals: globals.browser } },
];
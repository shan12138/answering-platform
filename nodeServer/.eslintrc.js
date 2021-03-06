module.exports = {
  "env": {
    "browser": true,
    "commonjs": true,
    "es6": true,
    "node": true,
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": 2016,
    "sourceType": "module",
  },
  "rules": {
    "indent": ["error", 2],
    "quotes": ["error", "single"],
    "semi": ["error", "never"],
    "no-cond-assign": ["error", "always"],
    "no-console": "off",
  }
}
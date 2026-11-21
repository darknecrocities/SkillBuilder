# ICU MessageFormat, Pluralization & Cultural Formatting Manual

> **Objective**: Eliminate broken string concatenation (`items.length + " items"`), gender/plural grammar bugs, and ambiguous date/currency formatting across all world locales.

---

## 1. Strict ICU MessageFormat Rules

Never assemble translated UI copy by joining fragments in code (`"You have " + n + " files"` breaks word order in Japanese, German, and Arabic). Always pass structured arguments into a single ICU message:

```icu
{itemCount, plural,
  =0 {No records match your filter.}
  one {# verified record found.}
  other {# verified records found.}
}
```

### Mandatory Plural Rules
- Always provide `other` (required fallback in every CLDR locale).
- Never assume `one` means `n === 1` — in French `0` and `1` use `one`, while in Russian `21`, `31`, `101` also map to `one`, and `few`/`many` are mandatory.
- Use `select` for grammatical gender or role variants rather than concatenating pronouns.

---

## 2. Native `Intl` Formatters (Zero Moment.js Bloat)

| Domain | Production Pattern | Notes |
| :--- | :--- | :--- |
| **Currency** | `new Intl.NumberFormat(locale, { style: "currency", currency }).format(amount)` | Store money in integer minor units (cents/centavos), never floats. |
| **Dates & Time** | `new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeZone }).format(date)` | Always pass explicit `timeZone` (`Asia/Manila`, `UTC`) for server SSR parity. |
| **Relative Time** | `new Intl.RelativeTimeFormat(locale, { numeric: "auto" })` | Renders `"yesterday"` / `"kahapon"` cleanly without external libs. |
| **Collation / Sort** | `new Intl.Collator(locale, { sensitivity: "base" }).compare(a, b)` | Respects accented characters (`ñ`, `é`, `ü`) accurately. |

---

## 3. Dictionary Completeness & Key Safety
- Enable compile-time key checking (e.g., `next-intl` / typed `Record<Locale, Dictionary>`) so missing translation keys fail CI rather than rendering raw `nav.unknownKey` strings to users.

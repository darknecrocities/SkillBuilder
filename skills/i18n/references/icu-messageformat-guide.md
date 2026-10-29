# ICU MessageFormat & Pluralization Guide

ICU MessageFormat provides standard syntax for parameter interpolation, pluralization, and gender selection across world locales.

---

## 1. Pluralization Syntax

```icu
{itemCount, plural,
  =0 {You have no unread items.}
  one {You have # unread item.}
  other {You have # unread items.}
}
```

### Supported Categories:
`zero`, `one`, `two`, `few`, `many`, `other`.
Different language families (e.g., Slavic, Arabic, Romance) use different sets of categories. Always support `other` as the catch-all.

---

## 2. Number & Date Formatting

- Currency: `{amount, number, ::currency/USD}`
- Percentages: `{rate, number, ::percent}`
- Dates: `{eventDate, date, ::yyyyMMdd}`

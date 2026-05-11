# Frontend Slides

> Zero-dependency, animation-rich HTML presentations in a single file.

## When to activate

Trigger on: creating presentations, slide decks, pitch decks, conference talks, teaching materials, converting PPTX to HTML, or enhancing existing slides.

## Non-negotiables

1. **Zero dependencies** — default to one self-contained HTML file with inline CSS and JS.
2. **Viewport fit is mandatory** — every slide must fit inside one viewport with no internal scrolling. Use `height: 100vh`.
3. **Show, don't ask** — discover style through visual previews, not questionnaires. Generate 3 single-slide samples for the user to pick from.
4. **No generic templates** — prioritize distinctive aesthetics over cookie-cutter layouts.
5. **Production quality** — accessible, responsive, performant code.

## Process

### 1. Detect mode
- **New** — building from scratch
- **Convert** — PPTX/PDF → HTML
- **Enhance** — improving existing HTML slides

### 2. Discover content
Clarify before building:
- Purpose: pitch / teaching / conference / internal share
- Length: number of slides
- Content state: outline ready, full text ready, or needs drafting

### 3. Discover style
Unless user has a known preset:
- Generate **3 single-slide preview files** with different aesthetics
- Let user pick or mix elements
- Save chosen style as a preset name for reuse

### 4. Build
Output a single `.html` file with:
- Semantic HTML structure
- CSS custom properties (variables) for easy theming
- Navigation: keyboard (←→), touch swipe, mouse wheel
- Intersection Observer for reveal animations
- `prefers-reduced-motion` support
- Type hierarchy using `clamp()` for responsive sizing
- Atmospheric backgrounds over illustrations

### 5. Content density caps

| Slide type | Maximum content |
|------------|----------------|
| Title slide | 1 heading + 1 subtitle |
| Content slide | 1 heading + 4-6 bullets OR 2 short paragraphs |
| Grid/cards | 6 cards maximum |
| Code slide | 8-10 lines maximum |
| Image slide | 1 image + 1 caption |

### 6. Validate
Test across 5 breakpoints:
- 1920×1080 (desktop)
- 1440×900 (laptop)
- 1024×768 (tablet landscape)
- 768×1024 (tablet portrait)
- 375×667 (mobile)

Every slide must pass viewport fit at all sizes.

### 7. Deliver
Provide:
- File path to the HTML file
- Preset name (for future reuse)
- Slide count
- Customization guidance (how to change colors, fonts, content)

## Technical structure

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Presentation Title]</title>
  <style>
    :root {
      --primary: #...;
      --secondary: #...;
      --bg: #...;
      --text: #...;
      --font-heading: ...;
      --font-body: ...;
    }
    /* All styles inline */
  </style>
</head>
<body>
  <div class="slide" id="slide-1">...</div>
  <div class="slide" id="slide-2">...</div>
  <script>
    // Navigation, animations, all inline
  </script>
</body>
</html>
```

## Navigation features

- **Keyboard**: ← → arrow keys, Space, Enter
- **Touch**: swipe left/right
- **Mouse**: wheel scroll
- **Progress**: visual indicator (dots or bar)
- **Slide counter**: current / total

## PPTX conversion workflow

1. Read PPTX content (extract text, images, layout)
2. Map each slide to appropriate HTML template
3. Preserve content hierarchy
4. Apply chosen style preset
5. Export images as inline base64 or separate files
6. Validate viewport fit for all converted slides

## Style presets (examples)

- **Dark minimal** — dark bg, light text, subtle gradients
- **Corporate clean** — white bg, brand colors, structured
- **Bold creative** — vibrant colors, large type, dynamic animations
- **Academic** — serif fonts, muted tones, content-dense

// jasa.typ
// A simplified Typst template for JASA (Acoustical Society of America)

#let jasa(
  title: "",
  authors: (),
  abstract: none,
  // date: datetime.today().display(),
  preprint: true, // Set to false for "Reprint" (two-column) style
  bib-file: none,
  bib-style: "apa", // JASA uses APA (author-year) or numeric
  body,
) = {
  // --- 1. Setup Variables based on Preprint/Reprint ---
  let font-size = if preprint { 12pt } else { 10pt }
  let lead-size = if preprint { 1.5em } else { 0.65em } // Line spacing
  let col-count = if preprint { 1 } else { 2 }
  let gutter-size = 0.5in
  let line-nums = if preprint { "1" } else { none } // Only show line numbers in preprint

  // --- 2. Page & Text Settings ---
  set document(title: title, author: authors.map(a => a.name))
  set page(
    paper: "us-letter",
    margin: 1in,
    numbering: "1",
  )

  set text(
    font: "Times New Roman", // JASA standard font
    size: font-size,
    lang: "en",
  )

  // Paragraph formatting
  set par(
    leading: lead-size,
    justify: true,
    first-line-indent: 1.5em,
  )

  // Turn on line numbering for preprints
  set par.line(numbering: line-nums, step: 5)

  // --- 3. Heading Styles ---
  // JASA Level 1: Centered, Uppercase, Bold
  show heading.where(level: 1): it => {
    set align(center)
    set text(weight: "bold", size: font-size)
    block(above: 1.5em, below: 1em)[
      #upper(it)
    ]
  }

  // JASA Level 2: Left aligned, Bold
  show heading.where(level: 2): it => {
    set align(left)
    set text(weight: "bold", size: font-size)
    block(above: 1.2em, below: 0.8em, it)
  }

  // JASA Level 3: Italic, Bold
  show heading.where(level: 3): it => {
    set text(weight: "bold", style: "italic", size: font-size)
    block(above: 1em, below: 0.6em, it)
  }

  // Numbering style (I. A. 1.)
  set heading(numbering: "I.A.1.")

  // --- 4. Math Styling ---
  show math.equation: set text(weight: "regular")
  set math.equation(numbering: "(1)")

  // --- 5. Content Rendering ---

  // Title Block (Always single column)
  align(center)[
    #v(1em)
    #text(size: 1.2em, weight: "bold")[#title]
    #v(1em)

    // Authors
    #(
      authors
        .map(a => [
          #text(weight: "bold")[#a.name] \
          #text(style: "italic", size: 0.9em)[#a.affiliation]
        ])
        .join([\ \ ])
    )

    // Date
    // #v(0.5em)
    // #text(size: 0.9em)[#date]
  ]

  // Abstract
  if abstract != none {
    v(1.5em)
    align(center)[*Abstract*]
    pad(x: 2em)[#abstract]
    v(1.5em)
  }

  // Main Body (Columns applied here if reprint)
  show: columns.with(col-count, gutter: gutter-size)

  body

  // Bibliography
  if bib-file != none {
    bibliography(bib-file, title: "References", style: bib-style)
  }
}

# V0.4 Frontend UI Design Spec

## 1. Design Direction

V0.4 treats the product as a multi-user knowledge column platform, not a single-person blog or an admin console. The visual language follows the supplied UI reference image: clean, modern, restrained, content-first, and suitable for a course project presentation.

Core adjectives:

- Clean: generous spacing, clear information hierarchy, low visual noise.
- Modern: card-based layout, unified navigation, refined form controls.
- Restrained: soft blue-violet accent, light borders, subtle shadows, no neon colors.
- Knowledge community: articles, columns, authors, tags, comments, and search all feel like equal parts of the same product.
- Demo-friendly: every page should immediately communicate its purpose.

The UI must avoid default browser styling, default blue underlined links, naked buttons, naked inputs, and old-fashioned HTML list pages.

## 2. Layout Rules

- Global page max width: use `1120px` for dense content and up to `1200px` for wider product sections.
- Main content is centered with consistent horizontal padding.
- Header is shared by all public/user pages and remains sticky at the top.
- Page sections use clear vertical rhythm: normal sections around `56px-72px`, compact sections around `32px-40px`.
- Home page structure:
  - Unified top navigation.
  - Hero area with platform positioning.
  - Prominent search bar.
  - Primary action: start reading.
  - Secondary action: become a creator.
  - Feature cards.
  - Latest articles.
  - Recommended columns.
  - Platform philosophy.
  - Footer.
- Article list, search, category, and tag pages use a main list plus optional right sidebar.
- Column list uses a card grid and must feel like a creator-facing public product page.
- Article detail page uses a comfortable reading column and a right sidebar for author, table of contents, and related column information.
- Auth pages use a centered card with a lightweight illustration/product panel.
- Write article page uses an editor workspace layout, with a prominent title field, spacious body editor, and clear publish/draft actions.

## 3. Component System

All pages should reuse the same component classes.

- Header:
  - Sticky, white translucent background, subtle border, compact nav links.
  - Brand mark plus product name.
  - Search icon/input area.
  - Login/register/user actions on the right.
- Search Bar:
  - Rounded 8px-12px.
  - Light border, soft background, clear focus ring.
  - Used in header, hero, article list, and search page.
- Buttons:
  - Primary button uses blue-violet brand color.
  - Secondary button uses white/transparent background with brand border.
  - Ghost/text button is allowed for quiet navigation.
  - Buttons need hover, focus, active, and disabled states.
- Article Card:
  - Title, summary, author, category, tags, time, view/comment placeholders.
  - Prefer horizontal layout on list/search pages and compact grid layout on home.
- Column Card:
  - Column name, description, creator, article count, follower placeholder, entry button.
  - Should communicate that ordinary users can create columns.
- User Card:
  - Avatar placeholder, nickname, bio, article count, column count.
- Tag:
  - Rounded pill with light background and hover state.
- Category Badge:
  - Small brand-tinted pill or outlined badge.
- Comment Card:
  - White card/row, reviewer status wording, author name, time, content.
- Auth Card:
  - Centered, white card, strong title, clear form labels, full-width primary submit.
- Editor Form:
  - Large title field, spacious body editor, grouped metadata side panel.
- Empty State:
  - Light dashed/solid panel with concise message and optional action.
- Footer:
  - Product name, version, course-project positioning, and public navigation links.

## 4. Visual Rules

- Remove default blue underlined links across public pages.
- Use CSS variables for all core colors and shared dimensions.
- Use 8px border radius for cards and controls unless a pill shape is semantically appropriate.
- Use light borders and subtle shadows; avoid heavy drop shadows.
- Avoid excessive gradients. Gradients may be used only as soft section backgrounds.
- Avoid fluorescent colors and one-note palettes.
- Text hierarchy:
  - Hero headline: large but controlled.
  - Page title: strong, compact.
  - Card title: medium weight, readable.
  - Metadata: muted and compact.
- Reading pages prioritize line length, line height, and content contrast.

## 5. Interaction States

All primary interactive elements must define:

- Hover: color, border, background, or shadow changes.
- Focus: visible focus ring for keyboard users.
- Active: slightly pressed or darker state.
- Disabled: reduced opacity and no pointer interaction.

This applies to buttons, links, inputs, selects, textareas, article cards, column cards, tag pills, and pagination.

## 6. Responsive Rules

- Desktop: multi-column layouts, sidebars where useful.
- Tablet: grids wrap naturally, sidebars move below content.
- Mobile: single-column layout, full-width buttons when needed, compact nav.
- Navigation must not squeeze or overlap.
- No horizontal scrollbar is allowed.
- Fixed-format UI elements such as cards, toolbars, stats, and form actions must use stable dimensions and responsive constraints.

## 7. Page-Level Acceptance Notes

- Home communicates: every user can create a knowledge column.
- Articles page uses a modern list/card layout with search and sidebar filters.
- Columns page presents public creator columns, not admin management.
- Article detail is a reader page with comments and sidebar context.
- Login/register pages are productized auth experiences, not bare forms.
- Write article page feels like a writing tool.
- User profile shows avatar, bio, stats, articles, and columns.
- Search results separate article, column, and user result types where data is available.
- AI functionality remains out of scope for V0.4.

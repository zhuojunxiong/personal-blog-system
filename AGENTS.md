# AGENTS.md

## Project Background

This project is a course practice project named "AI-assisted Personal Blog System Design and Implementation".

The first version should be a runnable, demo-friendly, and extensible V0.1 system. It should prioritize a complete core workflow over many loosely connected features.

## Core Principles

1. Build the runnable main workflow first, then extend features.
2. Keep code modular. Do not put all functionality in one file.
3. Route modules receive requests, call services, and return responses.
4. Service modules hold business logic.
5. Model modules hold database structures.
6. AI features must be isolated behind an AI service interface.
7. Comments, search, dashboard statistics, and AI behavior should be replaceable independently.
8. Keep the implementation easy to explain in reports and presentations.

## Tech Stack

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLite first, MySQL later
- Jinja2
- Bootstrap

## V0.1 Scope

Must support:

- Public article list
- Article detail page
- Category browsing
- Tag browsing
- Keyword search
- Admin login and logout
- Article CRUD
- Category management
- Tag management
- Visitor comments
- Comment review
- Mock AI summary generation
- Mock AI tag recommendation
- AI operation logs

Do not implement yet:

- Normal user registration
- Multi-user community features
- Likes, favorites, follows, private messages
- Frontend-backend separation
- Real AI API dependency
- Cloud deployment

## Database Requirements

The database must include at least:

- User
- Article
- Category
- Tag
- ArticleTag
- Comment
- AiLog

Tags must use a many-to-many relationship with articles. Do not store tags as a plain string on the article table.

Comments must have a review status and must not appear publicly before approval.

Passwords must be stored as hashes, never plaintext.

AI outputs must be logged with input, output, adoption status, and room for manual correction notes.

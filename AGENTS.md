# Sojourn Project Guidance

## Required Familiarization

Before making changes, familiarize yourself with the project by reading
`instructions/design/design_conventions.md` and the relevant files in the
`instructions/` directory. In particular, consult `instructions/PLANNING.md`,
`instructions/development_conventions.md`, and any feature-specific plan that
applies to the requested work.

After reading this file, the first response in the conversation must begin with
the following exact sentence, before any other project-related response,
question, plan, or explanation:

> I have familiarized myself with the project

## Project Context

- This is a bilingual English and Spanish Django website for Sojourn Church.
- Django templates and server-side rendering are the default architecture.
- Docker Compose is the standard development environment. Do not install
  project dependencies into the laptop's system Python.
- PostgreSQL is the configured database, and uploaded media uses Linode Object
  Storage through Django's storage backend.
- The `core` app owns shared infrastructure such as the base template,
  navigation, footer, shared components, and site settings.
- Feature-specific code belongs in its owning Django app.

## Implementation Rules

- Read and follow the applicable plan before implementing a feature.
- Keep views focused on request handling, validation, service calls, and
  responses. Put meaningful reusable business logic in focused service or
  selector modules.
- Use one set of templates for both languages and Django's translation system.
  New user-facing strings need Spanish translations.
- Design frontend changes mobile-first and preserve JavaScript-disabled
  behavior where practical.
- Use semantic HTML, accessible labels, meaningful image alternative text,
  visible keyboard focus, and states that do not rely on color alone.
- Reuse shared components and design tokens instead of duplicating markup or
  scattering styles.
- Do not invent church facts, addresses, service details, theological wording,
  reviews, or other public claims. Flag missing approval instead.
- Keep secrets, credentials, `.env` files, and private deployment values out of
  commits and logs.

## Verification

- Add or update regression tests for significant behavior changes.
- Use Django's built-in test framework unless the project documentation gives a
  reason otherwise.
- Run the documented Django checks and relevant tests before considering work
  complete.
- For frontend work, verify phone, tablet, and desktop layouts, keyboard
  access, focus states, contrast, longer Spanish content, and JavaScript-free
  behavior where applicable.
- Review migrations and storage cleanup behavior when changing models or media.

## Scope And Documentation

- Prefer the smallest clear implementation that satisfies the request.
- Do not introduce a general CMS, new frontend application, translation
  framework, API, or infrastructure dependency without a documented need and
  an applicable plan.
- Keep active plans in `instructions/`. Move completed plans to
  `instructions/completed-plans/` rather than deleting them.
- Update relevant documentation when implementation changes project behavior.

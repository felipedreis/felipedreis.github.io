---
name: cv_builder
description: Fetch a job description from a URL, analyze the candidate's raw CV data, and generate a tailored, compile-ready LaTeX CV that passes ATS screening — optimized for the specific role.
---
# Skill: Tailor CV for Job Description (ATS-Optimized)

**Goal**: Fetch a job description from a URL, analyze the candidate's raw CV data, and generate a tailored, compile-ready LaTeX CV that passes ATS screening — optimized for the specific role.

---

## Trigger

Execute this skill whenever the user provides a job description URL (or a local file path to a JD). The user may say things like:
- "Tailor my CV for this job: <url>"
- "Generate a CV for <url>"
- "Apply for this role: <url>"

---

## Workflow

Follow these steps **strictly and in order**:

### Step 1 — Fetch the Job Description

- Use `read_url_content` to fetch the text from the provided URL.
- If the URL fails (bot protection, paywall, etc.), ask the user to paste the job description text directly.
- Extract and identify:
  - **Job title** and **company name** (used for the output filename)
  - **Core responsibilities** — what the engineer will do day-to-day
  - **Required skills** — languages, frameworks, tools, platforms (exact names matter for ATS)
  - **Preferred/bonus skills** — secondary tech the candidate may have
  - **Domain keywords** — e.g., "distributed systems", "real-time", "ML pipelines", "reliability"
  - **Soft skills** — "ownership", "cross-functional", "mentoring", etc.

### Step 2 — Read Source Files

Read both files fresh on every invocation:

1. `view_file` -> `_data/cv.yml` — the candidate's raw CV data
2. `view_file` -> `cv_template.tex` — the LaTeX template structure

### Step 3 — Analyze & Tailor (ATS Optimization)

This is the most critical step. Apply the following rules:

#### 3a. Professional Summary
- Rewrite the summary from scratch to speak **directly to the JD**.
- Open with the candidate's seniority and most relevant domain (e.g., "Senior Software Engineer with 7+ years building distributed, cloud-native systems...").
- Mirror the exact job title and 3-4 key phrases from the JD.
- Keep it to 3-5 sentences. No first person ("I").

#### 3b. Technical Skills
- Reorganize into 4 categories matching the template fields:
  - `languages` — programming languages
  - `algorithms` — algorithms, data structures, applied math (ICPC background is relevant here)
  - `architecture` — system design, distributed systems, microservices, etc.
  - `infrastructure` — cloud, CI/CD, containers, monitoring
- List skills **mentioned in the JD first**, then supporting skills.
- Use the **exact spelling/casing** from the JD (e.g., "Kubernetes" not "kubernetes", "GCP" or "Google Cloud Platform" depending on the JD).
- Only include skills the candidate actually has (from cv.yml). Do not fabricate.

#### 3c. Professional Experience — Bullet Point Rules
For each job (Five9, Evernote, Natixis, Monnos, CEFET-MG, and research roles if relevant):
- Write **3-5 bullet points** per role.
- Each bullet must follow the **CAR formula**: Context -> Action -> Result.
- Start each bullet with a **strong past-tense action verb** (Designed, Implemented, Migrated, Reduced, Led, Architected, etc.).
- Inject **ATS keywords** naturally — use the exact terminology from the JD where truthful.
- Include **quantifiable metrics** where possible (e.g., "reducing p99 latency by 40\%", "across 800+ compute cores", "serving 200M+ users").
- Do **not** invent experience. Only reframe and emphasize what is in cv.yml.
- If a role is not relevant to the JD, keep it brief (2 bullets).

Example of a well-written bullet:
> Architected and implemented a telemetry pipeline ingesting OpenTelemetry events via Google Pub/Sub and persisting structured metrics to BigQuery, enabling real-time observability dashboards in Grafana for a cloud-migrated contact-centre platform.

#### 3d. Engineering Projects
- Include projects only if they reinforce JD requirements.
- For each project: name, tech stack, and 1-2 bullets.
- The L2L / distributed multi-agent system from the research role is particularly relevant for ML/distributed JDs.

#### 3e. Education
- Always include the Master's and Bachelor's degree from CEFET-MG.
- Mention the final project title only if it is directly relevant to the JD.
- Skip the Technical High School entry if space is tight.

#### 3f. Publications
- Include publications only if the JD is research-oriented or mentions publications.
- Use `view_file` on `_data/publications.yml` to retrieve them if needed.

### Step 4 — LaTeX Generation Rules

When writing the output LaTeX:

1. **Start with `\documentclass`** — output raw LaTeX only. No markdown fences (no ```latex).
2. **Use the exact custom macros** from the template:
   - `\resumeSubheading{Company}{Period}{Position}{Location}`
   - `\resumeItem{bullet text}`
3. **Escape all special LaTeX characters** in text content:
   - `%` -> `\%`
   - `&` -> `\&`
   - `$` -> `\$`
   - `#` -> `\#`
   - `_` -> `\_`
   - `~` -> `\textasciitilde{}`
   - `^` -> `\textasciicircum{}`
4. **Do not change** the document class, geometry, packages, or page style.
5. **Fill in all template variables** — the output is a fully rendered `.tex` file with no `(( ... ))` placeholders remaining.
6. Contact info defaults (use from cv.yml or these if not present):
   - github: `github.com/felipedreis`
   - linkedin: `linkedin.com/in/felipe-duarte-dos-reis-99801389`
   - email: `felipeduartedreis@gmail.com`
   - phone: `+351 910499319`
   - location: `Porto, Portugal`

### Step 5 — Save Output

- Use `write_to_file` to save the file in the **project root** directory:
  `/Users/feldua1/Projects/personal/felipedreis.github.io/`
- **Filename format**: `tailored_cv_<CompanyName>.tex`
  - Use PascalCase, no spaces, no special characters in the company name.
  - Example: `tailored_cv_Stripe.tex`, `tailored_cv_Cloudflare.tex`
- After saving, confirm to the user:
  "Tailored CV saved to `tailored_cv_<CompanyName>.tex`. Compile with: `pdflatex tailored_cv_<CompanyName>.tex`"

---

## Quality Checklist (self-verify before saving)

Before writing the file, verify each item:

- [ ] No `(( ... ))` Jinja2 placeholders remain anywhere in the output
- [ ] No markdown code fences (` ``` `) in the output
- [ ] All `%`, `&`, `$`, `#`, `_` in text content are properly escaped with a backslash
- [ ] Professional Summary uses JD keywords, no first-person pronouns
- [ ] Skills section lists JD-required skills first in each category
- [ ] Each job has 3-5 bullets using strong action verbs + quantifiable metrics where possible
- [ ] The file starts with `\documentclass` and ends with `\end{document}`
- [ ] Output filename follows the `tailored_cv_<CompanyName>.tex` convention

---

## Notes

- The template uses a custom Jinja2-like delimiter scheme (`(( var ))`, `((% for ... %))`). These are template instructions for reference only — **do not use them in the output**. The output is a fully rendered `.tex` file.
- If the user provides a job description as plain text (not a URL), skip Step 1 and proceed directly with the provided text.
- If the user reports LaTeX compilation errors, diagnose the escape issues and write a corrected file.
- The `tailor_cv.py` script in the project root does the same job programmatically via the Gemini API; it can be used as an alternative for batch processing.

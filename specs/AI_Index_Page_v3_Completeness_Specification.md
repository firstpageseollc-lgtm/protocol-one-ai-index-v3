# AI Index Page v3 — Completeness Specification

**Status:** DRAFT FOR BRANDON'S REVIEW — not ratified, not yet a Protocol One standard  
**Date:** 2026-10-26  
**Prepared for:** Brandon Frost, Protocol One  
**Supersedes:** Nothing. AI Index Page v2 remains valid.  
**Purpose:** Define what makes an AI Index Page *complete* without making it merely longer.

{^}

---

## 1. Executive summary

AI Index Page v2 solved the **container**:

- a binary opening that identifies Protocol One, states the format version, explains how to read the page, and carries the business's Alfa Code;
- an English body for humans;
- an executable Python body for machines;
- a binary closing containing a timestamp and a SHA-256 integrity seal.

V3 addresses the next problem: the **record inside the container**.

A v3 page should let a human, an AI system, or a verifier determine:

1. **What business this is** — identity, locations, contacts, and canonical addresses.
2. **What it offers** — products, services, prices, limits, and availability.
3. **How it operates** — hours, service area, booking or ordering paths, policies, and support.
4. **Where each critical fact came from** — owner approval, source, and last verification date.
5. **Whether this is the current version** — page version, status, review date, and what it supersedes.
6. **Whether the page is intact** — the v2 integrity seal, retained and strengthened by parity checks.
7. **How other systems can consume it** — derived JSON-LD/schema.org and llms.txt outputs generated from the same canonical source.

### The v3 completeness rule

> **An AI Index Page is complete when every critical public fact is present, internally consistent, owner-approved, sourced, current, and traceable to one canonical sealed version.**

Completeness does **not** mean:

- every conceivable fact is included;
- the facts are guaranteed true;
- an AI system will rank, recommend, cite, or update from the page by any particular time;
- private or sensitive information is exposed.

The page controls the facts AI systems can read. Its seal proves integrity. Its provenance shows who approved the record and when it was checked. Neither the seal nor the page proves the underlying claims are true.

---

## 2. Canon preserved from v2

V3 must preserve the confirmed v2 design unless Brandon separately decides to change it.

### 2.1 Confirmed v2 elements

- The binary is a **trust envelope**, not decoration.
- The binary start is the opening/handshake and address.
- The binary end is the closing/seal.
- The bookends mirror Tri-Signature: Intent opens, Confirmation closes.
- The middle is English for humans and Python for machines.
- The start identifies Protocol One and the format version, explains how to read the page, and carries the business's Alfa Code.
- The end carries a timestamp and integrity seal.
- The seal is SHA-256 over the English and Python body bytes.
- AI Index Pages are the AI-facing discovery and presentation surface for a business and, for Protocol One itself, for the wider ecosystem.
- An Alfa Code follows ratified Specification v0.1 syntax when one is issued:  
  `ALFA-<ISSUER>-<CLASS>-<GEO>-<ZONE>-<SERIAL6>-<CHECK2>`
- A candidate or pending Alfa Code must be labeled as such. It must never be presented as formally issued before assignment and logging are complete.

### 2.2 Protocol One laws applied

- **No identity without an event:** publication requires an identifiable owner-approval event or an explicitly recorded approval reference.
- **No silent change:** a correction creates a new page version and a new seal. The prior version is superseded, never silently rewritten.
- **Verification needs no permission:** anyone holding the page can verify its structure, seal, parity, status fields, and provenance fields without an account or a Protocol One server.
- **Every chain starts and ends with a human:** a human owner or authorized representative approves the opening record; a human approves material closure, replacement, or withdrawal.

---

## 3. Design principles

### 3.1 One canonical source

The AIP is the canonical business record. Websites, JSON-LD, llms.txt, platform profiles, and verification pages may render or derive from it, but they do not become competing sources of truth.

Every derived output must carry:

- the canonical page URL;
- the AIP record version;
- the AIP SHA-256 digest;
- a generated-at timestamp;
- the notice: `Derived output — verify against the canonical AI Index Page.`

### 3.2 Public facts only

An active public AIP contains facts the business has approved for public use.

It must not contain:

- government identifiers;
- bank, tax, or payment credentials;
- private home addresses not already used publicly for the business;
- personal contact details that the individual has not approved for publication;
- precise geocoordinates by default, consistent with Alfa Code v0.1;
- trade secrets, internal procedures, or customer information;
- passwords, keys, tokens, or recovery information.

### 3.3 Owner-approved does not mean independently true

Every critical fact must have an approval and provenance status. The page must distinguish:

- what the owner asserted and approved;
- what was checked against an official source;
- what is bound to a document or DocLock record;
- what remains unverified.

Unverified facts may exist in a draft. They must not be represented as verified in an active page.

### 3.4 English and Python are equal representations

The English and Python bodies are two renderings of the same record, not two separate records. Critical facts must agree across both bodies before sealing.

### 3.5 Completeness is modular

Every page has a required universal core. Additional modules are required only when they apply to the business type or operating model. A solo lawyer should not be forced to publish restaurant fields; a restaurant should not be forced to publish legal-intake fields.

### 3.6 Freshness is part of completeness

A page can be intact and still be stale. V3 therefore treats review status as a separate axis from seal integrity:

- **CURRENT** — the review date has not passed.
- **REVIEW DUE** — the review date is within the warning window or has just passed.
- **STALE** — the review date has passed beyond the allowed grace period.
- **UNKNOWN** — no review date is present. This is acceptable only for a legacy or draft page, not for a fully complete active v3 page.

### 3.7 No rankings promise

No AIP copy, sales material, verifier output, or derived export may promise rankings, citations, recommendations, model inclusion, or update timing. The honest claim is control over the canonical facts made available to AI systems.

---

## 4. V3 envelope specification

## 4.1 Physical order

```text
[BINARY START]
[ENGLISH BODY]
[PYTHON BODY]
[BINARY END]
```

No new body is added between the English and Python bodies. Provenance, lifecycle, and interoperability metadata are represented in:

1. the binary-start header JSON;
2. structured sections of the English body;
3. structured data in the Python body;
4. derived external exports, when generated.

This preserves the recognizable v2 form.

## 4.2 Binary start

The v3 binary start retains the v2 structure and changes the version byte to `3`.

```text
Magic:          "AIP1"                         4 bytes
Version:        3                              1 byte
Header length:  unsigned big-endian integer    4 bytes
Header:         UTF-8 JSON                     header length
English length: unsigned big-endian integer    4 bytes
Python length:  unsigned big-endian integer    4 bytes
Digest:         SHA-256(English bytes + Python bytes)  32 bytes
```

### 4.2.1 Required header fields

| Field | Type | Rule |
|---|---|---|
| `protocol` | string | Must be `Protocol One`. |
| `logo` | string | Must be exactly `{^}`. |
| `format` | string | Must be `AI Index Page`. |
| `version` | integer | Must be `3`. |
| `how_to_read` | string | Must explain the order, bodies, seal, and verification method. |
| `business` | string | Public display name of the business. |
| `legal_name` | string or null | Required when different from the display name or when the page makes legal-identity claims. |
| `alfa_code` | string or null | Required for a fully complete active page unless Brandon approves an exception. Candidate status must be explicit. |
| `alfa_code_status` | string | One of `issued`, `candidate`, `pending_assignment`, `not_assigned`, or `not_applicable`. |
| `canonical_url` | string | The canonical public URL of this AIP. |
| `record_id` | string | Stable identifier for the business's AIP record; does not change between versions. |
| `record_version` | string | Version of this business record, using the scheme in §7. |
| `record_status` | string | One of `draft`, `active`, `superseded`, or `withdrawn`. |
| `language` | string or array | Primary language and any additional published languages. |
| `issued_by` | string | Normally `Protocol One`. |
| `completeness_class` | string | The class claimed under §10. The builder must not claim a class whose checks have not passed. |

### 4.2.2 Optional but recommended header fields

| Field | Purpose |
|---|---|
| `supersedes_digest` | SHA-256 digest of the immediately preceding version, when one exists. |
| `supersedes_record_version` | Human-readable prior version. |
| `doclock_record_id` | DocLock record binding for the issued page, when one exists. |
| `approval_ref` | Reference to the owner-approval event or record. It identifies the approval; it does not expose private approval evidence. |
| `time_status` | `local_only`, `attested`, or `not_attested`, describing any separate time-attestation reference. It must not imply the closing timestamp itself is attested unless a valid attestation reference is present. |
| `review_by` | Date by which the record should be reviewed. |
| `module_set` | List of vertical or operating modules included in the page. |

## 4.3 English body

The English body must be readable without executing code. It presents the same canonical facts as the Python body in the section order defined in §5.

## 4.4 Python body

The Python body must be valid Python and expose one primary record named `BUSINESS`.

It may expose pure helper functions for reading the record, such as:

- `summary()`
- `get_product(sku)`
- `get_service(service_id)`
- `get_location(location_id)`
- `is_open(weekday, location_id=None)`
- `canonical_record()`

### 4.4.1 Python safety profile

The Python body:

- must not import modules;
- must not read or write files;
- must not access the network;
- must not execute system commands;
- must not contain credentials or secrets;
- should contain data and pure, deterministic helper functions only.

A public verifier should prefer parsing and static validation over unrestricted execution. If execution is offered, it must occur in a restricted environment.

## 4.5 Binary end

The v3 binary end retains the v2 structure:

```text
Magic:           "1PIA"                         4 bytes
Timestamp length: unsigned big-endian integer   4 bytes
Timestamp:        ISO-8601 UTC                  timestamp length
Digest:           SHA-256(English + Python)     32 bytes
```

The closing timestamp records when this version was sealed.

### 4.5.1 Time distinction

The closing timestamp alone is **not** attested time. A page may reference a separate DocLock or CryptoLock attestation, but the reference must state its own status honestly:

- `LOCAL-ONLY`
- `ATTESTED`
- `ATTESTATION-MISMATCH`

A v3 page must not describe a local closing timestamp as atomic, certified, or independently attested.

---

## 5. Canonical content model

The English and Python bodies must implement the following sections. A section may be marked `not_applicable` only when the reason is recorded in the builder's intake record; public copy does not need to list irrelevant sections.

## 5.1 Document control

Required information:

- business display name;
- record ID;
- record version;
- record status;
- canonical AIP URL;
- format version;
- completeness class;
- sealed timestamp, after sealing;
- correction contact;
- review-by date;
- summary of what changed in this version.

## 5.2 Identity — Who and Where

Required core fields:

| Field | Notes |
|---|---|
| `name` | Public display name. |
| `legal_name` | Legal entity name when applicable. |
| `entity_type` | LLC, corporation, sole proprietor, partnership, nonprofit, individual professional, or other accurate type. |
| `description` | Plain-language description of the business. |
| `tagline` | Optional; omit rather than invent. |
| `founded` | Year or date, only when approved and supportable. |
| `public_owner_or_founder` | Include only when the business wants the person publicly identified. |
| `alfa_code` | Address in the Protocol One object-world layer, with status. |
| `canonical_url` | This AIP's canonical URL. |
| `website_url` | Main public website, when one exists. |
| `locations` | One or more public business locations or an explicit online/service-area model. |
| `service_area` | Geographic area served, without precise private coordinates by default. |
| `contact_channels` | Public phone, email, contact form, booking page, or other approved channels. |
| `languages` | Languages in which the business serves customers. |
| `official_profiles` | Canonical social, marketplace, map, or professional profiles. |

### Location object

Each location should support:

- stable location ID;
- public label;
- street address, when public;
- city, state or region, postal code, and country;
- phone and email specific to that location;
- hours reference;
- accessibility information, when known and approved;
- parking or arrival notes, when useful;
- whether walk-ins, appointments, pickup, delivery, or remote service are available.

## 5.3 Offer — What

The page must describe the offer precisely enough for an AI system to avoid inventing products, services, or prices.

### Product object

Each product should support:

- stable product ID or SKU;
- name;
- description;
- product type;
- price and currency, when public;
- pricing basis, such as each, per hour, per project, starting at, or fixed package;
- effective date for time-sensitive pricing;
- canonical product URL;
- availability status;
- what is included;
- what is not included;
- delivery method;
- file manifest for digital products, when applicable.

### Service object

Each service should support:

- stable service ID;
- name;
- description;
- intended customer;
- price or price range, when public;
- pricing basis;
- canonical service URL;
- availability;
- prerequisites;
- deliverables;
- exclusions;
- expected process;
- booking or inquiry path.

### Negative offer facts

The page should explicitly state material things the business does **not** do when confusion is likely. Examples:

- no shipping outside a stated region;
- no emergency service;
- no walk-ins;
- no representation in a particular matter type;
- no sale of a discontinued product;
- no guarantee of a particular result.

Negative facts are often as valuable as positive facts because they prevent AI systems from filling gaps with guesses.

## 5.4 Operations — When and How

Required when applicable:

- regular hours, with timezone;
- holiday or seasonal exceptions, when known;
- ordering, booking, intake, or consultation path;
- lead time;
- delivery, pickup, shipping, or remote-service rules;
- payment methods, without payment credentials;
- cancellation policy;
- return or refund policy;
- support channel and expected response window;
- accessibility information;
- service limitations;
- emergency instructions or explicit non-emergency status, when relevant.

Hours must never be published without a timezone when the business serves customers across locations or online.

## 5.5 Questions and decision facts

Each page should answer the standard AI question battery for its business type:

1. What is this business?
2. Where is it located or where does it operate?
3. What does it sell or do?
4. What does it cost, or how is pricing determined?
5. When is it open or available?
6. Who owns, leads, or represents it publicly?
7. How does a customer contact, book, order, or begin?
8. What does it not offer?
9. What has changed recently?
10. Why would a customer choose it over an alternative?

Answers must be factual. Comparative or promotional claims require a source or owner-approved basis and must not be disguised as neutral facts.

The Python body should expose these as a structured `questions` or `faq` list when they are not already unambiguously represented in other fields.

## 5.6 Boundaries and do-not-claim rules

Every active page should include a `do_not_claim` list when there are known risks of misdescription.

Examples by industry:

- A law firm: do not promise an outcome; do not describe educational content as legal advice; do not claim a specialization unless properly supported.
- A restaurant: do not claim allergen safety beyond the kitchen's stated practice; do not publish a menu item that is not currently offered.
- A technology company: do not claim certifications, integrations, performance rates, or regulatory status that have not been established.
- Protocol One: do not claim SOC 2 or ISO certification, a false-accept rate, patent-pending status, or that DocLock proves content truth.

The do-not-claim list is guidance to AI readers. It does not guarantee model behavior.

## 5.7 Legitimate action paths

An AIP identifies where legitimate action occurs. It does not become ACP and does not issue commands.

Permitted action-path fields include:

- canonical booking URL;
- canonical ordering URL;
- canonical contact URL;
- phone number;
- intake URL;
- directions URL;
- support URL;
- eligibility notes that a human or AI should check before beginning.

Action paths must be canonical or owner-approved. Affiliate, tracking, or short links should not replace the canonical destination; tracking parameters may be recorded separately in campaign systems.

---

## 6. Provenance model

## 6.1 Provenance unit

Provenance may be recorded at section level by default. Critical facts may carry individual provenance when the risk or likelihood of confusion justifies it.

Critical facts include:

- legal identity;
- ownership or founder identity;
- addresses and service area;
- prices and pricing conditions;
- hours;
- credentials, licenses, and certifications;
- product availability;
- policies that affect money, safety, or legal rights;
- canonical contact and action paths.

## 6.2 Provenance fields

Each provenance record should contain:

| Field | Meaning |
|---|---|
| `subject` | Field, section, product, service, or location covered. |
| `status` | `owner_approved`, `source_checked`, `document_bound`, or `unverified`. |
| `source_type` | `owner_assertion`, `official_website`, `government_registry`, `professional_registry`, `source_document`, `platform_record`, or `other`. |
| `source_ref` | Public URL or non-sensitive document/record reference. Private evidence is referenced, not embedded. |
| `approved_by` | Name or role of the approving person, as approved for the record. |
| `approved_at` | Date or timestamp of approval. |
| `last_verified_at` | Date or timestamp when the fact was last checked. |
| `review_by` | Date by which it should be checked again. |
| `approval_ref` | Optional Tri-Signature event, DocLock record, or other approval reference. |
| `notes` | Short limits or qualifications. |

## 6.3 Provenance statuses

### `owner_approved`

The business owner or authorized representative reviewed and approved the fact for publication. This is the minimum status for a critical fact in an active page.

### `source_checked`

The fact was compared with an identified source. The source and check date must be present.

### `document_bound`

The fact is supported by a document or record bound through a DocLock record or another identified evidence reference. This status describes the binding; it does not independently prove the statement is true.

### `unverified`

The fact has not been approved or checked. It may appear in a draft only and prevents the page from claiming full completeness.

## 6.4 Owner approval

Before an active v3 page is sealed, the owner or authorized representative must approve:

- the business identity;
- every critical fact;
- the public contact and action paths;
- the do-not-claim list;
- the Alfa Code status;
- the record version and change summary.

The approval may be recorded as a simple approval reference in v3. A Tri-Signature event reference is the preferred Protocol One form when available, but v3 does not require inventing one where no event exists.

---

## 7. Lifecycle and versioning

## 7.1 Record identity

Each business has one stable `record_id`.

Recommended form:

```text
AIP-<ISSUER-OR-BUSINESS-CODE>-<SHORT-STABLE-ID>
```

The exact record-ID issuance rules remain an open decision in §14. The record ID is separate from the Alfa Code:

- the **Alfa Code** identifies the business or object in the world layer;
- the **record ID** identifies the AIP document record;
- the **record version** identifies one issued state of that record;
- the **SHA-256 digest** identifies the exact sealed bodies of that version.

## 7.2 Record version

Recommended version form:

```text
<major>.<minor>
```

- Increment **major** when facts are removed, materially corrected, reclassified, or when the offer, identity, location, or policies materially change.
- Increment **minor** for additions or clarifications that do not materially change the meaning of existing facts.
- A formatting-only republication should not occur silently. If the sealed bodies change, the version and seal change.

## 7.3 Status values

| Status | Meaning |
|---|---|
| `draft` | Not approved for public reliance. May be incomplete or unverified. |
| `active` | The current approved public version. |
| `superseded` | Replaced by a newer version. The page remains verifiable as a historical record. |
| `withdrawn` | No longer offered as a current record. The reason and effective date should be recorded. |

Only one version of a record should be active at a canonical URL at a time.

## 7.4 Change log

Each new version must include a concise change summary:

- facts added;
- facts corrected;
- facts removed;
- prices or hours changed;
- locations added or removed;
- policies changed;
- provenance refreshed;
- format or export changes.

The change log belongs in the English body and as structured data in the Python body.

## 7.5 Review periods

Review periods should be set by volatility and risk, not by a universal fiction that all facts age at the same speed.

Draft defaults for Brandon's decision:

| Business or fact type | Suggested review period |
|---|---:|
| Prices, menus, inventory, hours | 30–90 days |
| Law-firm practice, credentials, intake rules | 90–180 days |
| Stable identity and location facts | 180–365 days |
| Safety, licensing, or regulated claims | At or before the governing renewal or change date |

The page carries one overall `review_by` date, normally the earliest review date among its critical sections.

---

## 8. English/Python parity

## 8.1 Critical-field parity set

Before sealing, the builder must compare at least:

- display and legal names;
- Alfa Code and status;
- canonical URLs;
- addresses and service area;
- contact channels;
- hours;
- product and service names;
- SKUs and stable IDs;
- prices, currencies, and pricing bases;
- availability;
- major inclusions and exclusions;
- policies;
- record version and status;
- provenance statuses and dates;
- do-not-claim items.

## 8.2 Parity outcomes

| Outcome | Meaning |
|---|---|
| `MATCH` | All critical fields agree. |
| `NONCRITICAL_DIFFERENCE` | Wording differs but no critical field conflicts. The difference is recorded in the build report. |
| `MISMATCH` | A critical field conflicts. The page must not be sealed as active until corrected. |

## 8.3 Build report

Every issued page should have an internal build report recording:

- builder and schema versions;
- checks run;
- parity outcome;
- completeness class awarded;
- provenance coverage;
- unresolved warnings;
- export digests;
- publication URL;
- verification result after publication.

The build report is operational evidence. It does not need to be embedded in the public page.

---

## 9. Interoperability and derived exports

## 9.1 Canonical rule

Exports are derivatives. They improve reach but never replace the AIP.

An export must be regenerated after any new AIP version is sealed. An export whose embedded AIP digest does not match the current active AIP is stale and must not be presented as current.

## 9.2 JSON-LD / schema.org export

Generate a JSON-LD representation using the closest accurate schema.org types, such as:

- `Organization`
- `LocalBusiness`
- `LegalService`
- `Attorney`
- `Restaurant`
- `Store`
- `Product`
- `Service`
- `Offer`
- `FAQPage`, only when the page contains genuine question-and-answer content

Rules:

- Do not add ratings, reviews, awards, or credentials that are not in the canonical AIP.
- Do not force a business into a more specific schema type than the facts support.
- Preserve currency, price basis, availability, and canonical URLs.
- Include the AIP canonical URL and digest in a clearly identified provenance property or accompanying manifest.

## 9.3 llms.txt export

Generate a concise llms.txt derivative containing:

- business name;
- one-paragraph description;
- canonical website and AIP links;
- main products or services;
- location and service area;
- contact and action paths;
- a link to the full AIP.

The llms.txt export is a discovery aid. It is not sealed as the canonical record unless separately issued as one.

## 9.4 Human web rendering

A normal HTML page may render the English body and verification summary for visitors who should not have to inspect a text artifact.

The rendering must identify:

- that the AIP is the canonical record;
- the record version and status;
- the sealed date;
- the review status;
- the verification result;
- a link or tool for independent verification.

## 9.5 Discovery checklist

Publication is not complete until the following are checked:

- canonical AIP returns successfully;
- canonical URL is stable;
- footer, navigation, or another durable internal link points to the AIP where appropriate;
- sitemap includes the AIP or an equivalent discovery path exists;
- robots or platform settings do not unintentionally block it;
- derived exports point to the current AIP digest;
- the public verification view resolves to the active version.

Inclusion in a sitemap or crawl does not guarantee that any AI model will read, retain, cite, or update from the page.

---

## 10. Completeness classes

V3 uses gates, not a misleading single percentage.

## 10.1 Class C0 — Draft

- May be incomplete.
- May contain unverified facts.
- Must be labeled draft.
- Must not be sold or represented as a completed active page.

## 10.2 Class C1 — Structurally complete

Requirements:

- valid v3 envelope;
- valid English and Python bodies;
- required universal core fields present;
- applicable modules present;
- Python safety profile passes;
- English/Python parity passes;
- seal verifies.

C1 answers: **Is the record well-formed and internally consistent?**

## 10.3 Class C2 — Publication complete

All C1 requirements, plus:

- owner approval recorded for every critical fact;
- Alfa Code issued or its candidate/pending status accurately disclosed;
- canonical URL live;
- discovery checklist passed;
- do-not-claim list present where a known misdescription risk exists;
- no `unverified` critical facts.

C2 answers: **Is the record approved and properly published?**

## 10.4 Class C3 — Provenance complete

All C2 requirements, plus:

- provenance present for every critical fact or critical section;
- source type and reference recorded where a source exists;
- approval date and last-verified date present;
- review-by date present;
- DocLock or approval reference present when the delivery package claims one.

C3 answers: **Can a reader tell who approved this, what it was checked against, and when?**

## 10.5 Class C4 — Lifecycle managed

All C3 requirements, plus:

- record version and change log present;
- supersession chain present after the first version;
- active status can be distinguished from superseded versions;
- derived exports match the active digest;
- freshness status is computable;
- a review or correction workflow is assigned.

C4 answers: **Can this record remain trustworthy as the business changes?**

### Recommended commercial baseline

The standard paid v3 delivery should target **C3**, with C4 available when Protocol One also manages reviews, re-seals, and exports over time. Pricing and packaging for those levels are separate Brandon decisions and are not set by this specification.

---

## 11. Vertical modules

## 11.1 Law firms and individual lawyers

Additional fields:

- firm or practice legal name;
- attorney names and roles, when public;
- bar admissions and license jurisdictions, when claimed;
- practice areas;
- matter types accepted;
- matter types not accepted;
- consultation types and fees, when public;
- intake path;
- conflicts-check notice;
- service jurisdictions;
- office locations and appointment rules;
- languages;
- professional profiles;
- advertising or jurisdictional disclaimers required for the practice.

Rules:

- No outcome promises.
- No description of general information as legal advice.
- No unsupported specialization or certification claim.
- The firm or lawyer approves every fact line by line before sealing.

## 11.2 Restaurants and food businesses

Additional fields:

- current menu or canonical menu URL;
- cuisine;
- price range;
- hours and kitchen-closing time, when different;
- reservation path;
- takeout and delivery options;
- service area and delivery partners, when applicable;
- allergen and dietary practice, stated carefully;
- catering availability;
- private-event availability;
- parking and accessibility;
- holiday hours.

Rules:

- Menu facts must carry an effective or last-verified date.
- Do not overstate allergen safety.
- A third-party delivery listing does not override the canonical restaurant record.

## 11.3 Retail and e-commerce

Additional fields:

- product catalog or canonical catalog URL;
- SKU and variant structure;
- inventory or availability basis;
- shipping regions;
- shipping times and costs, when public;
- returns and exchanges;
- digital-delivery method;
- product file manifests;
- support path;
- marketplace profiles.

Rules:

- Dynamic inventory must state how and when availability is determined.
- A static AIP must not pretend to be a real-time inventory system.

## 11.4 Professional and local services

Additional fields:

- services and service packages;
- credentials and licenses, when claimed;
- service area;
- estimate or consultation process;
- emergency availability or explicit non-emergency status;
- scheduling lead time;
- warranties or guarantees, only as actually offered;
- insurance claims, only when established;
- before-and-after or portfolio URLs, when approved.

## 11.5 Protocol One ecosystem pages

A Protocol One page may additionally expose:

- the relevant trust-stack layers;
- product or standard status;
- specification version;
- implementation status;
- what the layer proves;
- what it does not prove;
- canonical specification URL;
- related DocLock, Tri-Signature, Alfa Code, CryptoLock, ACP, or G.A.I.L. references.

Status language must distinguish clearly among:

- concept;
- draft specification;
- ratified specification;
- prototype;
- built and tested;
- live product;
- deprecated or superseded.

---

## 12. Verification specification

## 12.1 Verification inputs

A verifier receives one of:

- the AIP text or file;
- the canonical AIP URL;
- a prior version plus a claimed successor, for chain checks.

No account, permission, or Protocol One server is required for the core checks.

## 12.2 Checks

A v3 verifier should perform:

1. **Envelope parse** — magic, version, lengths, header JSON, closing structure.
2. **Digest check** — SHA-256 of the English and Python bodies matches both seals.
3. **Timestamp parse** — closing timestamp is valid ISO-8601 UTC.
4. **Header consistency** — header identity, Alfa Code, canonical URL, record ID, version, and status match the bodies.
5. **Python safety and structure** — valid Python, required record present, prohibited operations absent.
6. **Schema check** — required core and module fields present and correctly typed.
7. **Parity check** — critical English and Python fields agree.
8. **Alfa Code check** — syntax and check characters validate when an issued Alfa Code is claimed; candidate status is not misrepresented.
9. **Provenance check** — critical facts have the required approval/source/date fields for the claimed completeness class.
10. **Freshness check** — review-by date produces CURRENT, REVIEW DUE, STALE, or UNKNOWN.
11. **Lifecycle check** — status and supersession fields are coherent; a claimed successor or predecessor digest resolves when available.
12. **Export check** — derived exports carry the same record version and digest when exports are supplied.

## 12.3 Verification outputs

The verifier must not output a bare `TRUE` or `VERIFIED` without saying what was verified.

Recommended result fields:

```text
Envelope: VALID / INVALID
Integrity: INTACT / BROKEN
Parity: MATCH / MISMATCH / NOT CHECKED
Schema: COMPLETE / INCOMPLETE
Provenance: COMPLETE / PARTIAL / ABSENT / NOT CHECKED
Freshness: CURRENT / REVIEW DUE / STALE / UNKNOWN
Lifecycle: ACTIVE / SUPERSEDED / WITHDRAWN / DRAFT / UNKNOWN
Completeness class supported: C0 / C1 / C2 / C3 / C4
```

Example plain-language result:

> This page is intact and internally consistent. It is record version 1.2, owner-approved on 2026-10-20, last checked on 2026-10-24, and due for review by 2027-01-22. Verification confirms the record's integrity and provenance fields; it does not prove that every business claim in the record is true.

## 12.4 Failure language

- A digest mismatch is **BROKEN SEAL**.
- A missing required field is **INCOMPLETE**, not broken.
- A passed review date is **STALE** or **REVIEW DUE**, not broken.
- A replaced page is **SUPERSEDED**, not invalid merely because it is old.
- A fact dispute is a **correction issue**, not automatically an integrity failure.

These distinctions prevent the verifier from overstating what failed.

---

## 13. Authoring and publication workflow

### Step 1 — Intake

Collect facts, public sources, canonical URLs, locations, offers, policies, and the owner's public/private boundaries.

### Step 2 — Source map

Map every critical fact to its proposed source and approver. Flag conflicts between the website, platform listings, registries, and owner statements.

### Step 3 — Draft record

Build one structured source record. Generate the English and Python bodies from that record rather than editing them independently.

### Step 4 — Completeness and parity checks

Run schema, safety, parity, Alfa Code, and claims checks. Resolve critical mismatches before owner review.

### Step 5 — Owner review

The owner or authorized representative reviews the exact public wording and structured facts. Corrections return to the structured source record.

### Step 6 — Approval

Record the approval reference, approver, and date. When a Tri-Signature event or DocLock record is used, record its identifier without exposing private evidence.

### Step 7 — Seal

Generate the v3 envelope and closing timestamp. Run the full verifier against the sealed artifact.

### Step 8 — Publish

Publish at the canonical URL. Confirm the live page matches the sealed artifact exactly.

### Step 9 — Discovery and exports

Generate JSON-LD and llms.txt derivatives, update internal links and sitemap paths, and record export digests in the build report.

### Step 10 — Before/after AI audit

Where the commercial package includes it, run the agreed AI question battery before publication and again after an agreed interval. Report what changed without promising rankings or citations.

### Step 11 — Review and reissue

At review, confirm, correct, add, or remove facts in the structured source. Issue a new record version with a change log and a new seal. Mark the prior version superseded.

---

## 14. Open decisions for Brandon

This draft does not silently decide the following:

### OD-V3-1 — Commercial baseline

Should the standard paid v3 page target **C3 Provenance Complete**, with C4 lifecycle management as the managed/retainer level?

**Draft recommendation:** Yes.

### OD-V3-2 — Owner approval form

Is a recorded owner approval sufficient for C2/C3, or should a Tri-Signature event reference be required at C3 when the tooling is available?

**Draft recommendation:** Recorded approval is sufficient for v3 launch; Tri-Signature becomes the preferred and eventually required form at the highest provenance level when production capture is ready.

### OD-V3-3 — Provenance granularity

Should provenance be section-level by default, with fact-level provenance only for critical facts?

**Draft recommendation:** Yes. Fact-level provenance for every sentence would make pages heavy and hard to maintain.

### OD-V3-4 — Record ID syntax

Should the recommended `AIP-<business-code>-<stable-id>` form become canonical, or should record identity be derived from the Alfa Code plus a separate document sequence?

**Draft recommendation:** Keep record ID and Alfa Code separate. They identify different things.

### OD-V3-5 — Review periods

Are the suggested review windows in §7.5 correct by vertical, and who may extend a review date without a full reissue?

**Draft recommendation:** Only an owner-approved fact check can extend the date; the extension itself creates a new version if it changes sealed content.

### OD-V3-6 — Export status

Are JSON-LD and llms.txt standard derivatives of every v3 page, optional delivery extras, or internal publication tools?

**Draft recommendation:** Generate both for every active page; the AIP remains canonical.

### OD-V3-7 — Attested time

Should C4 require a DocLock/CLK-ATTEST-1 reference for the issuance event?

**Draft recommendation:** Not for the first v3 release. Record the time status honestly and add attestation when the workflow is operationally reliable for client pages.

### OD-V3-8 — Public verifier

Should the first public verifier be a Protocol One-hosted convenience tool, an offline downloadable tool, or both?

**Draft recommendation:** Both eventually; the offline verification rules and file format come first so the hosted tool is never the root of trust.

### OD-V3-9 — Legacy v2 upgrades

Should existing v2 pages be upgraded only during a paid refresh, or should Protocol One proactively offer v3 conversion to early customers?

**Draft recommendation:** Do not silently convert them. Offer conversion as a new owner-approved version.

### OD-V3-10 — Completeness labels

Are `C0–C4` the right public labels, or should the classes receive descriptive names only?

**Draft recommendation:** Use both in specifications and descriptive names in customer-facing material: Draft, Structurally Complete, Publication Complete, Provenance Complete, and Lifecycle Managed.

---

## 15. Backward compatibility and migration

- V2 pages remain valid under v2 rules.
- A v3 verifier must read v2 pages and report them as v2, not pretend they satisfy v3 provenance or lifecycle requirements.
- A v2 page is upgraded by creating a new v3 record version, not by editing the old sealed artifact.
- New facts and provenance claims in the v3 version require owner approval.
- The v3 version should record the v2 digest it supersedes when the v2 artifact is available.
- Existing canonical URLs may be retained when the new version replaces the old at the same address, provided the prior version remains available through an archive or version reference.

---

## 16. Acceptance tests for a future builder

A v3 builder is not complete until it passes at least the following tests:

1. Builds a valid v3 page from a structured source record.
2. Rejects a page with a missing required core field.
3. Rejects an active page containing an unverified critical fact.
4. Detects a one-character change in either body as a broken seal.
5. Detects an English/Python price mismatch before sealing.
6. Detects an invalid Alfa Code check segment.
7. Refuses to label a candidate Alfa Code as issued.
8. Produces JSON-LD and llms.txt exports carrying the correct AIP digest.
9. Detects a stale export after a new AIP version is issued.
10. Distinguishes CURRENT, REVIEW DUE, and STALE pages.
11. Distinguishes ACTIVE from SUPERSEDED versions.
12. Verifies a page offline without a Protocol One server.
13. Reads and reports a legacy v2 page without applying v3-only requirements retroactively.
14. Rejects Python containing imports, file access, network calls, or system execution.
15. Produces a build report listing every warning and the completeness class supported.

---

## 17. What v3 does not do

V3 does not:

- guarantee AI rankings, citations, recommendations, or model updates;
- prove that business claims are true;
- replace a business website, Google Business Profile, schema markup, or platform listings;
- replace DocLock, Tri-Signature, Alfa Code, CryptoLock, or ACP;
- define Deep Digital Language (DDL);
- authorize AI agents to act for the business;
- store private evidence inside a public page;
- turn a local timestamp into attested time;
- make a stale or superseded record current.

---

## 18. Draft conclusion

V2 made an AI Index Page a sealed, human-and-machine-readable artifact.

V3 makes it a **complete business record**:

- structured enough for machines;
- readable enough for humans;
- approved by the business;
- sourced and dated;
- explicit about limits;
- versioned as facts change;
- exportable to familiar AI and web formats;
- verifiable by anyone without permission.

That is the step from “a page AI can read” to “the canonical record AI should read first.”

---

*End of draft — awaiting Brandon's decisions on OD-V3-1 through OD-V3-10.*

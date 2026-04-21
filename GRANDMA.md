# GRANDMA.md
### *Explained like you're sitting across from me at the kitchen table*

---

## First, let me paint you a picture.

You know that feeling when the postman delivers a thick envelope — and inside
is a 30-page document from the bank, or a lease agreement, or some insurance
policy full of tiny print?

You sit down with a cup of tea. You start reading. By page 3, there are words
like *"indemnification clause"* and *"liability notwithstanding"* and your eyes
start to glaze over. You think: *I really should understand this before I sign it.*
But where do you even start?

Or maybe you're a small business owner. Every week, contracts come in.
Supplier agreements. Employment terms. Partnership proposals. Each one takes
hours to read properly. And if you miss one sentence — one little clause buried
on page 17 — it could cost you a lot of money.

**That is exactly the problem we built this tool to solve.**

---

## So what does it actually do?

We built a website — a real, working website you can open on any computer —
where you can upload any PDF document and let an AI read it for you.

Not skim it. Not pretend to read it. **Actually read every single word, on every
single page**, in about 10 seconds.

Then it immediately tells you:

### 📋 What the document is about
A short, clear summary in plain English. No jargon. No fluff. Just:
*"This is a 3-year supplier contract between Company A and Company B.
The main obligation is a monthly payment of $4,500 in exchange for
warehouse storage. Either party can exit with 60 days notice."*

Done. You understood a 22-page contract in two sentences.

---

### ⚠️ What could go wrong (the risks)
This is the part most people skip when reading — and it's the most important.

Our tool automatically highlights anything that looks dangerous. It colour-codes
them too:

- 🔴 **Red** = High risk — things like automatic renewal clauses that lock you in
  for another year if you don't cancel by a specific date
- 🟡 **Yellow** = Medium risk — things worth keeping an eye on
- 🟢 **Green** = Low risk — minor things, probably fine

Imagine having a careful lawyer friend who reads the document first and circles
all the dangerous bits before you even start. That's what this does — for free,
in seconds.

---

### 👤 Who is mentioned in the document
It picks out every name, every company, every city or address mentioned —
even if they appear once in a footnote on page 18. So you always know
exactly who is involved and where.

---

### 💰 Money and dates
Every amount of money. Every deadline. Every payment date. Pulled out and
listed clearly at the top, so you don't have to hunt for them yourself.

Imagine reading a contract and someone has already gone through it with a
yellow highlighter and circled every number and every date. That's what you see
the moment the document finishes loading.

---

### ✅ What you need to do next
The tool also lists *action items* — things the document is asking you or
someone else to do. Like:
- *"Submit signed copy by March 31st"*
- *"Provide proof of insurance within 14 days"*
- *"Review and approve the attached schedule"*

So even if you don't read a single page yourself, you know exactly what's
expected of you.

---

## But here's the really clever part.

After all that automatic analysis, you can **have a conversation with the document.**

You can type a question — in completely normal English, the way you'd ask a
person — and it answers you.

For example:

> *"What happens if I'm late on a payment?"*

And it replies with something like:

> **Answer:** A late fee of 1.5% per month is applied to the outstanding balance.
>
> **Evidence:** *"...any amounts not received within 15 days of the due date shall
> accrue interest at a rate of 1.5% per calendar month..."* *(Page 7)*
>
> **Confidence:** High — this was stated clearly and directly in the contract.

It doesn't just give you the answer. It shows you **exactly where in the document
it found it** — the actual sentence, with the page number — so you can go
check it yourself if you want. It never asks you to just trust it.
The system only answers using the document you upload, so it does not guess or invent information from outside sources.

And if the answer isn't in the document at all, it tells you that honestly.
It will never make something up.

---

## You can even compare two documents side by side.

Say you have two different quotes from two different suppliers. Upload both,
click Compare, and the tool will tell you:

- What they have in common
- Where they differ (especially on price, terms, and responsibilities)
- Which one looks riskier
- What to watch out for before you choose

Like having a trusted advisor read both and give you their honest opinion —
in under a minute.

---

## What if the AI has a bad day?

Good question! We thought of that.

Our tool actually has **two AI systems running behind the scenes**, not one.
The main one is Google's AI (very powerful, very fast). But if for any reason
Google's system is busy or unavailable, our tool automatically and silently
switches to a backup AI called Groq — without you even noticing.

It's like having a main doctor and a backup doctor always on call. You always
get seen, no matter what.

---

## What does it look like when you use it?

You open the website. You see a clean, dark-themed dashboard — a bit like a
mission control screen, but not confusing.

On the left, there's a panel where you drag and drop your PDF.

Ten seconds later, the main screen fills up with:
- A summary at the top
- A beautiful spider-web shaped chart showing the document's profile across
  6 dimensions (how risky it is, how urgent, how financially significant, and so on)
- A bar chart of the most important words in the document
- A little mood gauge showing whether the document's overall tone is positive,
  neutral, or negative (yes, even documents have a "mood")
- All the risks, people, organisations, dates, and money listed neatly

Then at the bottom, a chat box — just like texting — where you can ask
anything you want about what you just uploaded.

---

## Who is this for?

Honestly? Almost anyone.

- **A grandmother** who just received a long letter from her pension provider
  and wants to know if anything has changed
- **A small business owner** who doesn't have time to read every contract
  word for word
- **A student** who has to read a 50-page research report and needs the key
  points fast
- **Anyone** signing something important and wanting to make sure they're
  not missing anything

The goal is simple: **no one should have to sign something they don't
understand, just because it was too long to read.**

---

## What did we use to build it?

We wrote it in a language called Python — one of the most popular coding
languages in the world today. We connected it to Google's AI brain and Groq's
AI brain. We built the whole website interface ourselves. We handled the
document reading, the chunking (cutting the document into manageable pieces),
the searching, the charts, the chat — everything.

From a blank screen to a fully working, deployable web application.


---

## One last thing, Grandma.

If you ever get a long confusing document and you're not sure what it means —
send it to us. We built exactly the right tool for that.

*With love, your grandchild who spent way too many late nights staring at
a computer screen so that reading boring documents could finally be
just a little bit less boring.* 💜

---

*Built for the CST4625 Generative AI Hackathon.*

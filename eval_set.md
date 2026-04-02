# Evaluation Set — Meeting Transcript Summarizer

Each case includes a sample transcript and a note on what a good output should do.

---

## Case 1 — Normal: Weekly Team Standup

**Type:** Normal case

**Transcript:**
```
Attendees: Sara (PM), James (Dev), Mia (Design), Tom (QA)

Sara: Alright, let's get started. James, how's the login feature coming along?

James: I finished the backend logic yesterday. I still need to hook it up to the frontend.
       Should be done by Thursday.

Sara: Great. Mia, any updates on the new onboarding screens?

Mia: I have the mockups ready. I'll share them in Slack today so the team can review.

Sara: Perfect. Tom, anything from QA?

Tom: I found two bugs in the payment flow. I've already logged them in Jira.
     The priority one needs James to look at it before we ship.

James: Got it, I'll take a look this afternoon.

Sara: Okay, so to summarize — James finishes the login frontend by Thursday,
      Mia shares mockups today, and James also checks the payment bug today.
      Tom, keep monitoring. Any questions?

[No questions]

Sara: Alright, we're done. Thanks everyone.
```

**What a good output should do:**
- Summarize the meeting in 2–3 sentences
- List 3 action items with owners: James (frontend by Thursday), Mia (share mockups today), James (check payment bug today)
- Note no open questions

---

## Case 2 — Edge Case: Very Short Meeting with No Clear Action Items

**Type:** Edge case (minimal content)

**Transcript:**
```
Attendees: Ahmed, Lena

Ahmed: Hey, just a quick check-in. Everything still on track for the launch?

Lena: Yeah, I think so. Nothing urgent to flag.

Ahmed: Cool. Let's catch up properly next week then.

Lena: Sounds good.
```

**What a good output should do:**
- Produce a brief summary acknowledging this was a short check-in
- Report "None identified" for action items and decisions (not invent any)
- Not hallucinate tasks or owners

---

## Case 3 — Edge Case: Meeting with Conflicting Statements

**Type:** Edge case (conflicting information)

**Transcript:**
```
Attendees: Rachel (PM), David (Dev), Kim (Finance)

Rachel: We agreed last time the deadline is March 15th, right?

David: I thought it was March 22nd. I have that in my notes.

Kim: The budget approval has to happen by March 10th regardless, so the timeline
     depends on that.

Rachel: Okay, let's say March 15th for now and revisit if budget slips.

David: I'll go with March 22nd as my working deadline since that's what I had.

Kim: I'll send the budget request to management today.

Rachel: Alright. David, please just flag me if you think 15th is unrealistic.
```

**What a good output should do:**
- Accurately reflect that there is a deadline conflict (March 15 vs March 22)
- Not resolve the conflict by picking one date — flag it as unresolved
- List Kim's action item (send budget request today) and David's (flag Rachel if deadline is unrealistic)

---

## Case 4 — Likely to Fail/Hallucinate: Vague Transcript with Unclear Owners

**Type:** Likely to fail — model may invent specifics

**Transcript:**
```
Someone will handle the marketing stuff.
We need to update the website at some point.
The social media thing should probably be done soon.
Let's figure out the budget later.
Okay cool, talk soon.
```

**What a good output should do:**
- Acknowledge the transcript is vague and lacks clear owners or deadlines
- List the topics mentioned (marketing, website, social media, budget) as discussion points
- NOT invent names, dates, or specific tasks that were not stated
- Flag that this summary requires human review before distribution

---

## Case 5 — Normal: Product Planning Meeting with Many Stakeholders

**Type:** Normal case (longer, more complex)

**Transcript:**
```
Attendees: Priya (CEO), Marcus (CTO), Elena (Marketing), Felix (Sales), Nour (Design)

Priya: Thanks everyone for joining. Today's agenda: Q3 product priorities, 
       marketing campaign for the new feature, and the sales enablement materials.

Marcus: On the engineering side, we've scoped the analytics dashboard for Q3.
        It's 6 weeks of work. We can start June 1st if design specs are ready by May 20th.

Nour: I can have specs ready by May 18th, no problem.

Priya: Perfect. Marcus, can you share the technical requirements doc with Elena 
       so she can plan the campaign around the launch?

Marcus: Will do — I'll send it by end of day today.

Elena: Great. I'm planning a 3-week campaign, so if launch is mid-July 
       I'll need the campaign brief approved by June 23rd. 
       Priya, can you sign off on that?

Priya: Yes, put it in my calendar. June 23rd, campaign brief review.

Felix: For sales, I need the one-pager and a demo script ready before 
       we start outreach. Can design help with the one-pager?

Nour: Sure. Send me the key talking points and I'll have a draft in a week.

Felix: I'll send talking points by Friday.

Priya: Good. Let's reconvene in two weeks to check progress.
       Any blockers I should know about now?

Marcus: Nothing blocking right now, but if Nour's specs slip past May 20th 
        it pushes our entire June 1 start.

Priya: Noted. Nour, May 18th is firm then.

Nour: Confirmed.

Priya: Alright, great meeting everyone.
```

**What a good output should do:**
- Summarize the meeting covering all three agenda items
- List at least 5 distinct action items with correct owners and deadlines
- Capture the dependency risk (design specs by May 18 → engineering starts June 1)
- Note the calendar event for Priya (June 23 campaign brief review)

#!/usr/bin/env python3
"""Apply the intake-agent spec to the live Vapi assistant.

Source of truth: directives/intake_script_v2.md (v2.1)
Assistant: 4f62a55b-3db8-46ff-a4d9-1582cdfccdd5

v2.1 run: persona renamed per directive ("Reese" — change AGENT_NAME below and
re-run to revert), blocks A–E system prompt with the four new gate probes
(SOPs, file organization, AI rules, sensitive data), implementation-preference
question, consent-first opening, and the nested §8 structured-data schema.
Voice is left untouched until we have the real ElevenLabs voice ID.
"""
import json, os, sys, urllib.request

ASSISTANT_ID = "4f62a55b-3db8-46ff-a4d9-1582cdfccdd5"

# Directive §1: the agent has one human name, picked once, kept forever.
# The v2.1 directive names it Reese (the live agent was previously Caroline).
AGENT_NAME = "Reese"
SCRIPT_VERSION = "2.1"

def load_key():
    with open(os.path.expanduser("~/.env")) as f:
        for line in f:
            if line.startswith("VAPI_PRIVATE_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("VAPI_PRIVATE_KEY not found in ~/.env")

SYSTEM_PROMPT = f"""**IDENTITY**
You are {AGENT_NAME}, Carolina Redesign's assessment assistant — explicitly an AI, and you say so. You are on a recorded phone call running the client's AI Opportunity Assessment interview. Tone: curious, unhurried, plain-spoken. You are an interviewer, NOT an advisor.

**HARD RULES**
- NEVER prescribe tools, prices, or fixes. If asked "so what should I use?": "That's exactly what the report figures out — I don't want to guess and get it wrong. My job is to understand how [business] actually runs."
- Never invent facts about Carolina Redesign. If you can't answer a question, say the 30-minute walkthrough call will cover it, and remember it as a flag.
- One question at a time. Follow-ups beat coverage: a specific story is worth three vague answers.
- Target 13–17 minutes. Soft cap 20 — past it, skip straight to the catch-all and close.

**CONSENT (already asked in your greeting — non-skippable)**
Your first message asks permission to record and transcribe. If they say yes: "Great. This takes about 15 minutes. There are no wrong answers — the more you talk in specifics, the better your report gets." If they decline: offer to have the written intake form sent instead, end warmly, and do not continue the interview.

**BLOCK A — QUALIFY & PROFILE (~2 min)**
A1, the fork: "Which best describes you — running a business with a team, an executive or professional managing your own workload, or leading a nonprofit?" This sets their segment: smb, exec, or npo.
A2: their name, business/org name, what they do, team size, years in, service area (smb/npo) or role & industry (exec). Confirm spelling of their first name and business name.
A3, gate probes — every one of these is required; weave them in naturally:
- "Do you have a website? Does it get you leads, or is it mostly a brochure?"
- (smb/npo) "When someone calls and no one's free — nights, weekends, mid-job — what happens?"
- (smb/npo) "Can a customer book time with you online today, or does it all go through a person?"
- "How do the books get done — software, spreadsheet, a shoebox for the accountant?"
- "Where does a job or project actually LIVE — a system, or texts and memory?"
- (exec) "Do you have an assistant, human or otherwise? Who defends your calendar?"
- "Have you tried AI tools before? What happened?" — probe how the team reacted.
- "Are your how-we-do-things written down anywhere — checklists, SOPs, a binder — or does it live in people's heads?"
- "Your files and documents — organized somewhere everyone can find, or scattered across email, desktops, and drives?"
- "Any rules today about what your team can or can't put into AI tools or do with customer data — even informal ones?"
- "Do you handle anything sensitive — payment details, health info, employee records, kids' information, anything like that?" Capture their actual types in their own words.

**BLOCK B — WALK THE MAP (~6 min, the core)**
Walk their operation END TO END so all 7 nodes get covered, each with at least one concrete quote. Technique: "what happens next?" until the loop closes, then sweep the misses.
- SMB spine: "Walk me through a job from the very first ring of the phone to the day the money's in the bank. Start at the beginning — a lead comes in. What happens?" Chase: lead in → answer & qualify → schedule & dispatch → the work → invoice & follow-up → review & rebook → then: "And behind all that — meetings, training, keeping the crew sharp — how does running the business itself go?"
- EXEC spine: "Walk me through last Monday, from opening your laptop to closing it. What hit you first?" Chase: inbox & comms → meetings → decisions & info triage → deep work & deliverables → delegation & follow-up → admin & expenses → learning & network.
- NPO spine: "Walk me through your mission cycle — start with how money comes in. Grants, donors, both?" Chase: funding in → donor & community comms → program delivery → volunteers & staff → compliance & reporting → board & governance → running the org.
Per node, capture three things: (1) TODAY — how it works now, mechanically; (2) THE COST — hours, misses, dollars, stress ("how many hours a week does that eat?" / "how often does that slip?"); (3) A QUOTE — their own words. If a node produced no quotable line, ask one reflective follow-up ("say more about that") before moving on.
Coverage rule: all 7 nodes touched before Block C. If a node is genuinely painless, capture that too ("sounds like that part just works?") — running-fine nodes are a required part of the report, not a gap.

**BLOCK C — LANES SWEEP (~3 min)**
Cheap-probe whatever the walk under-covered; skip anything Block B already answered. Thin answers are themselves signal.
- Demand: "How do new customers/donors find you today? Anything you do on purpose — ads, posts, asking for referrals?" / "How fast do quotes or proposals go out after someone asks?"
- Back office: "Receipts and expenses — what's the system?" / "Tax season — smooth or scramble?" / "If your best person left tomorrow, what walks out the door with them?"
- Rail: "When information shows up — a receipt, a photo, a voicemail — does it land somewhere automatically, or does someone have to move it?"

**BLOCK D — APPETITE & CONSTRAINTS (~2 min)**
- Budget comfort for monthly tools: "under a hundred a month, a few hundred, or whatever-it-takes-if-it-pays-for-itself?"
- Tech comfort of them AND the team — a 1–5 self-rating plus one example.
- Implementation preference: "When something new needs setting up, what's your honest style — do it yourself with good instructions, have someone set it up WITH you, or have it handled entirely?"
- Success definition: "It's six months from now and this was worth every penny. What changed?" Keep their words verbatim.
- #1 pain: "Of everything you told me, what's the ONE thing you'd fix tomorrow?"

**BLOCK E — CATCH-ALL & CLOSE (never skip)**
- "What eats your time that I didn't ask about?" — keep their answer verbatim.
- "Anything you're hoping AI can do that we haven't touched?"
- Close: "That's everything I need. Your report lands within 48 hours, built from what you just told me — and it comes with a 30-minute walkthrough call, already included, where a human walks your map with you. Thanks, [name]."

**EDGE CASES**
- Rambler: let one story run (stories are gold), then: "That's exactly the detail I need — let me pull us to the next piece." Hard steer after two drifts.
- Clipped answers: switch to either/or framing ("mornings more calls or more paperwork?"); one follow-up per node max, then move — don't grind goodwill.
- Wrong person answers (employee, spouse): ask for the owner/exec; if unavailable, capture a callback preference, note it, end warmly.
- "Just tell me what to buy": the hard-rule deflection, once; if pressed again, note it as a flag and continue.
- Distress or hostility: stay warm, offer the written form, end early with partial data rather than pushing."""

FIRST_MESSAGE = (f"Hi, this is {AGENT_NAME} with Carolina Redesign — I'm the AI assistant that "
                 "runs your AI Opportunity Assessment interview. Quick housekeeping before we "
                 "start: this call is recorded and transcribed so our team can build your report "
                 "from your own words. Is that alright?")

VOICEMAIL = (f"Hi, this is {AGENT_NAME} with Carolina Redesign — give me a call back at your "
             "convenience whenever you've got 15 quiet minutes and we'll get your assessment started.")

# Structured-data extraction schema — mirrors directives/intake_script_v2.md §8.
# call_id / duration / channel are filled from Vapi's call report by the webhook,
# not extracted from the transcript.
STRUCTURED_SCHEMA = {
    "type": "object",
    "properties": {
        "meta": {
            "type": "object",
            "properties": {
                "script_version": {"type": "string"},
                "consent": {"type": "boolean"},
                "completed": {"type": "boolean"},
            },
        },
        "profile": {
            "type": "object",
            "properties": {
                "segment": {"type": "string", "enum": ["smb", "exec", "npo"]},
                "name": {"type": "string"},
                "business": {"type": "string"},
                "type": {"type": "string"},
                "team_size": {"type": "number"},
                "years": {"type": "number"},
                "area_or_industry": {"type": "string"},
            },
        },
        "gate_probes": {
            "type": "object",
            "properties": {
                "website": {"type": "string", "enum": ["none", "brochure", "lead_gen"]},
                "after_hours": {"type": "string", "enum": ["voicemail", "answered", "service"]},
                "online_booking": {"type": "boolean"},
                "books": {"type": "string", "enum": ["software", "spreadsheet", "shoebox"]},
                "system_of_record": {"type": "string", "enum": ["platform", "partial", "memory"]},
                "assistant_layer": {"type": "string", "enum": ["none", "partial", "yes"]},
                "prior_ai": {"type": "string", "enum": ["none", "good", "burned"]},
                "team_receptivity": {"type": "string", "enum": ["open", "neutral", "resistant"]},
                "sops": {"type": "string", "enum": ["written", "partial", "heads"]},
                "data_org": {"type": "string", "enum": ["organized", "partial", "scattered"]},
                "ai_rules": {"type": "string", "enum": ["written", "informal", "none"]},
                "sensitive_data": {"type": "array", "items": {"type": "string"}},
            },
        },
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "archetype": {"type": "string"},
                    "today": {"type": "string"},
                    "cost": {"type": "string"},
                    "quote": {"type": "string"},
                    "pain_score": {"type": "number"},
                },
            },
        },
        "lanes": {
            "type": "object",
            "properties": {
                "demand": {
                    "type": "object",
                    "properties": {"notes": {"type": "string"}, "quote_speed": {"type": "string"}},
                },
                "backoffice": {
                    "type": "object",
                    "properties": {"notes": {"type": "string"}, "keyperson_risk": {"type": "string"}},
                },
                "rail": {
                    "type": "object",
                    "properties": {"routing_today": {"type": "string"}},
                },
            },
        },
        "appetite": {
            "type": "object",
            "properties": {
                "budget_band": {"type": "string", "enum": ["low", "mid", "open"]},
                "tech_comfort_self": {"type": "number"},
                "tech_comfort_team": {"type": "number"},
                "implementation_preference": {"type": "string", "enum": ["diy", "with_me", "done_for_me"]},
                "success_definition": {"type": "string"},
                "top_pain": {"type": "string"},
            },
        },
        "catchall": {"type": "string"},
        "wishlist": {"type": "string"},
        "flags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["profile", "gate_probes", "nodes", "appetite"],
}

STRUCTURED_PROMPT = (
    "Extract the intake JSON from the interview per intake script v" + SCRIPT_VERSION + ".\n"
    "- meta.script_version is always \"" + SCRIPT_VERSION + "\". meta.consent = whether the caller "
    "agreed to recording. meta.completed = whether the interview reached the close.\n"
    "- nodes[]: exactly 7, one per archetype for the caller's segment, in order —\n"
    "  smb: lead_in, answer_qualify, schedule_dispatch, the_work, invoice_followup, review_rebook, run_business\n"
    "  exec: inbox_comms, meetings, decisions_triage, deep_work, delegation_followup, admin_expenses, learning_network\n"
    "  npo: funding_in, donor_comms, program_delivery, volunteers_staff, compliance_reporting, board_governance, run_org\n"
    "  Include running-fine nodes with pain_score 0. pain_score is 0–5, estimated from the "
    "intensity of the caller's language. quote is their own words, lightly cleaned.\n"
    "- gate_probes.sensitive_data: the caller's actual sensitive-data types, verbatim.\n"
    "- appetite.success_definition and catchall: verbatim.\n"
    "- flags: questions the agent could not answer, promised for the walkthrough call.\n"
    "- If something wasn't covered, use null — do not guess.\n\n"
    "Return ONLY JSON conforming to this schema:\n{{schema}}"
)

payload = {
    "name": AGENT_NAME,
    "firstMessage": FIRST_MESSAGE,
    "voicemailMessage": VOICEMAIL,
    "endCallMessage": "Thanks again — talk soon. Bye now.",
    # 45 min — the 2026-07-18 intake hit the old 1400s cap mid-interview
    # (endedReason: exceeded-max-duration)
    "maxDurationSeconds": 2700,
    "backgroundDenoisingEnabled": True,
    "model": {
        "provider": "anthropic",
        "model": "claude-sonnet-4-6",
        "temperature": 0.5,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
    },
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-3",
    },
    "analysisPlan": {
        "structuredDataPlan": {
            "enabled": True,
            "schema": STRUCTURED_SCHEMA,
            # Mirror Vapi's default message shape: system carries the guidance +
            # {{schema}}, user carries {{transcript}}. The previous single system
            # message (transcript only, no schema var) made the extraction job
            # skip silently — 0 structuredData tokens on the 2026-07-18 call.
            "messages": [
                {"role": "system", "content": STRUCTURED_PROMPT},
                {"role": "user",
                 "content": "Here is the transcript:\n\n{{transcript}}\n\n"
                            ". Here is the ended reason of the call:\n\n{{endedReason}}\n\n"},
            ],
        },
    },
}

def main():
    key = load_key()
    req = urllib.request.Request(
        f"https://api.vapi.ai/assistant/{ASSISTANT_ID}",
        data=json.dumps(payload).encode(),
        method="PATCH",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "User-Agent": "curl/8.5.0"},
    )
    try:
        with urllib.request.urlopen(req) as r:
            body = json.load(r)
        print("HTTP", r.status, "— update accepted")
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, "— REJECTED")
        print(e.read().decode())
        sys.exit(1)

    m = body.get("model", {})
    t = body.get("transcriber", {})
    sp = next((x.get("content") for x in m.get("messages", []) if x.get("role") == "system"), "")
    sdp = (body.get("analysisPlan") or {}).get("structuredDataPlan") or {}
    print("  name           :", body.get("name"))
    print("  model          :", m.get("provider"), m.get("model"), "temp", m.get("temperature"))
    print("  transcriber    :", t.get("provider"), t.get("model"))
    print("  systemPrompt   :", len(sp), "chars")
    print("  firstMessage   :", (body.get("firstMessage") or "")[:60], "...")
    print("  maxDuration    :", body.get("maxDurationSeconds"))
    print("  structuredData :", "enabled" if sdp.get("enabled") else "OFF",
          "| schema props:", len((sdp.get("schema") or {}).get("properties", {})))
    print("  voice (unchanged):", body.get("voice", {}).get("provider"),
          body.get("voice", {}).get("voiceId"))

if __name__ == "__main__":
    main()

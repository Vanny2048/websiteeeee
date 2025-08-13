import json
import random
from pathlib import Path

random.seed(42)

SLANG_PREFIXES = [
    "fr fr",
    "tbh",
    "ngl",
    "low-key",
    "imo",
]
SLANG_ENDINGS = [
    "no cap",
    "for real",
    "vibes",
    "kinda depends",
    "heads up",
    "pro tip",
]

BUILDINGS = [
    "Seaver Science Center",
    "University Hall (U-Hall)",
    "Life Sciences Building (LSB)",
    "William H. Hannon Library",
    "Burns Recreation Center",
    "Gersten Pavilion",
    "Sullivan Field",
    "Page Stadium",
    "Burns Aquatics Center",
    "Lair Marketplace",
    "The Bluff",
]

DINING = [
    "Lair Marketplace",
    "The Lion's Den",
    "The Bluff-side carts",
]

EVENTS = [
    "Wellness Wednesday",
    "Involvement Fair",
    "Career & Internship Fair",
    "Family Weekend",
    "Homecoming",
    "LMU Madness",
]

SERVICES = {
    "OneCard": [
        ("can my visitor use my OneCard?", "nah, OneCards are personal. Your visitor needs a guest pass or they pay their own way."),
        ("can I lend my OneCard to a roommate?", "don’t. it’s tied to you and can get flagged—bad vibes."),
        ("what can I do with OneCard?", "door access, dining, printing, laundry, events—pretty much your LMU passport."),
    ],
    "Mail": [
        ("where do I pick up packages?", "U-Hall P2 or the Campus Mail Center depending on the carrier—watch your email for pickup."),
        ("do they text for packages?", "email for sure; texts if you set it up—keep notifications on."),
        ("can someone else pick up for me?", "you’ll need proper authorization—staff won’t hand over without it."),
    ],
    "Printing": [
        ("how do I print on campus?", "upload to the print portal, tap your OneCard at a printer, collect and bounce."),
        ("does printing cost money?", "yeah, small per-page fee—load funds on your OneCard."),
        ("can guests print?", "limited options—LMU accounts work best. Check IT policies."),
    ],
    "Laundry": [
        ("does laundry take OneCard?", "yup—tap and go. Bring dryer sheets if you’re about that life."),
        ("are laundry rooms crowded?", "peak hours get spicy—late nights or mornings are chill."),
        ("can I get laundry alerts?", "some machines support app notifications—handy when it works."),
    ],
}

ACADEMICS_QA = [
    ("can I switch majors easily?", "depends—some programs are capped; talk to advising and plan ahead."),
    ("are minors flexible?", "usually easier—juggle prereqs and you’re good."),
    ("how does add/drop work?", "windows open in the portal—deadlines move quick, set reminders."),
    ("are there research opportunities?", "SURP and faculty-led projects are a thing—email profs with a solid pitch."),
    ("do waitlists move?", "sometimes—show up day one and message the prof respectfully."),
    ("pass/no pass allowed?", "policy exists with deadlines—may not count for major cores."),
]

REC_QA = [
    ("is gym access free?", "Burns Rec is included once you sign the waiver—get those gains."),
    ("how do I join intramurals?", "sign-ups open each term—teams fill fast so get in early."),
    ("is there a pool?", "Burns Aquatics has hours—check the schedule before you pack goggles."),
]

ATHLETICS_QA = [
    ("where do I get game tickets?", "athletics site has details—students often get discounts or free entries."),
    ("what conference is LMU in?", "WCC—rivalries make games a movie."),
    ("is there a student section?", "yup—Gersten gets loud. Wear school colors and bring energy."),
]

LIBRARY_QA = [
    ("what are Hannon Library hours?", "solid during the semester and extended for finals—peek the calendar."),
    ("can I book study rooms?", "yeah—reserve online, show up or you lose the slot."),
    ("are textbooks on reserve?", "some—check the catalog or ask the desk. Lifesaver during midterms."),
]

SAFETY_QA = [
    ("is campus safe at night?", "pretty good, but don’t be reckless—walk with friends and stay alert."),
    ("does LMU have safety escorts?", "Public Safety offers escorts after dark—clutch for late study sessions."),
    ("how do emergency alerts work?", "opt in via the portal—texts and emails go out fast when needed."),
]

AID_QA = [
    ("how do I contact financial aid?", "submit a ticket or call during hours—phones get answers faster, ngl."),
    ("is FAFSA required?", "for most aid, yeah—do it early and handle verification quick."),
    ("can I appeal my aid?", "if your situation changed—write a clear letter and include docs."),
]

CAREER_QA = [
    ("where’s career services?", "CPD has coaching, fairs, and workshops—book a slot and pull up."),
    ("are there on-campus jobs?", "tons—library, labs, rec, IT. Apply early before the best shifts vanish."),
    ("do alumni mentor students?", "yep—networking nights and platforms make it easy to link."),
]

ABROAD_QA = [
    ("can I study abroad?", "big yes—semester and summer options. Deadlines sneak up—apply early."),
    ("do credits transfer back?", "if pre-approved—get it in writing to keep the audit clean."),
    ("can STEM students go abroad?", "yup—map sequences so you don’t nuke your timeline."),
]

IT_QA = [
    ("how’s Wi‑Fi on campus?", "solid in academic buildings; dorms can be moody—ethernet helps."),
    ("how do I get IT help?", "submit a ticket or hit the help desk—walk-ins fix simple stuff fast."),
    ("can I print from my laptop?", "upload to the portal, release with OneCard, done."),
]

WELLNESS_QA = [
    ("does LMU have counseling?", "CAPS has sessions, groups, and referrals—it’s included, use it."),
    ("how long is the wait for therapy?", "varies—intake is quick, ongoing slots slow during finals."),
    ("are there wellness events?", "Wellness Wednesday and de-stress events pop up—check the calendar."),
]

DSS_QA = [
    ("what’s DSS?", "Disability Support Services—accommodations for tests, notes, housing, and more."),
    ("how do I get accommodations?", "apply with documentation; meet a coordinator; letters go to professors."),
    ("can I get extra test time?", "if approved—schedule ahead so rooms are ready."),
]

OISS_QA = [
    ("help for international students?", "OISS handles visas, work, and travel—they run solid info sessions."),
    ("can I work on an F‑1 visa?", "on-campus up to 20 hrs in term; CPT/OPT for internships—rules apply."),
    ("how do I keep status?", "full-time enrollment, valid I‑20, timely signatures—don’t slack."),
]

PARKING_QA = [
    ("is parking guaranteed with a permit?", "lol no—permits let you enter lots, not promise a spot."),
    ("is street parking a move?", "sometimes—watch signs in Westchester or you’ll donate to the city."),
    ("are scooters okay on campus?", "yeah, ride smart, don’t block entrances—lock it or lose it."),
]

DINING_QA = [
    ("is the meal plan worth it?", "if you’re on campus a lot, yes—Lair Marketplace becomes home base."),
    ("any vegan options?", "rotating plant-based options—menus change, check before you go."),
    ("late-night food on campus?", "some spots run late on weekdays—finals hours extend, clutch."),
]

SOCIAL_QA = [
    ("how’s the social scene at LMU?", "chill—dorm hangs, Greek life pockets, and LA nearby keep things moving."),
    ("what do people do on weekends?", "beach runs, Playa Vista food, and off-campus events—choose your vibe."),
    ("is it easy to make friends?", "join orgs, talk to RAs, show up—low-key that’s the whole play."),
]

CAMPUS_TIPS_QA = [
    ("best place to study?", "Hannon quiet floors, outdoor tables by LSB, random U-Hall nooks—try a few."),
    ("best way to not miss deadlines?", "sync Canvas to your calendar and set alarms—future you approves."),
    ("group project tips?", "assign roles, one shared doc, deadlines earlier than Canvas—trust me."),
]

WELLNESS_WEDNESDAY_VARIANTS_Q = [
    "when is Wellness Wednesday?",
    "what’s up with that Wellness Wednesday thing?",
    "Wellness Wednesday—worth going?",
    "what happens at Wellness Wednesday?",
    "how do I find Wellness Wednesday times?",
]
WELLNESS_WEDNESDAY_VARIANTS_A = [
    "Wellness Wednesday pops up during the term—check the events calendar for the latest time and spot.",
    "it’s a chill midweek reset—snacks, activities, good vibes—peep the calendar for this week’s details.",
    "if you like low-stress breaks and free stuff, yeah—watch the student emails for times.",
    "times shift by week—events page has the current schedule; show up when you can.",
]

SLANG_Q = [
    "what’s the move with {x}?",
    "is {x} a thing at LMU?",
    "{x}—worth it or nah?",
    "how do people handle {x} at LMU?",
    "real talk: {x}?",
]


def sprinkle(text: str) -> str:
    out = text
    if random.random() < 0.55:
        out = f"{random.choice(SLANG_PREFIXES)}, {out}"
    if random.random() < 0.35:
        out = f"{out}—{random.choice(SLANG_ENDINGS)}"
    return out


def distance_variations() -> list[dict]:
    out = []
    pairs = []
    tries = 0
    while len(pairs) < 120 and tries < 1000:
        a, b = random.sample(BUILDINGS, 2)
        if (a, b) not in pairs:
            pairs.append((a, b))
        tries += 1
    for a, b in pairs:
        mins = random.randint(4, 11)
        qs = [
            f"how far is it from {a} to {b}?",
            f"walk time {a} → {b}?",
            f"is {a} to {b} a hike?",
            f"how long from {a} to {b}?",
            f"could I scooter from {a} to {b}?",
        ]
        ans = [
            f"{a} to {b} is like a {mins}-minute walk if you’re not dragging. Scooters make it faster.",
            f"call it ~{mins} mins on foot—add a minute if you stop for bluff pics.",
            f"not bad—{mins}ish walking. Hills will humble you a bit.",
            f"you can scooter it easy—walking is around {mins} minutes.",
        ]
        for i in range(4):
            out.append({"instruction": qs[i % len(qs)], "output": sprinkle(ans[i % len(ans)])})
    return out


def service_variations() -> list[dict]:
    out = []
    for _svc, qas in SERVICES.items():
        for q, a in qas:
            vars_q = [q, q.replace("?", "—how does it work?"), q.replace("?", " (LMU)")] \
                     + [random.choice(SLANG_Q).replace("{x}", q.replace("?", "").strip())]
            vars_a = [a,
                      a + " Check the portal for specifics.",
                      a.replace(".", ", tbh.")]
            for vq in vars_q[:3]:
                out.append({"instruction": vq, "output": sprinkle(random.choice(vars_a))})
    return out


def generic_variations(base_qas: list[tuple[str, str]]) -> list[dict]:
    out = []
    for q, a in base_qas:
        qs = [q,
              q.replace("?", "—what should I know?"),
              q.replace("?", " (LMU)?"),
              q.replace("?", " in detail?"),
        ]
        ans = [a,
               a + " Check the site to be safe.",
               a.replace(".", ", imo.")]
        for vq in qs[:4]:
            out.append({"instruction": vq, "output": sprinkle(random.choice(ans))})
    return out


def events_variations() -> list[dict]:
    out = []
    for ev in EVENTS:
        for q in WELLNESS_WEDNESDAY_VARIANTS_Q:
            q2 = q.replace("Wellness Wednesday", ev)
            a2 = random.choice(WELLNESS_WEDNESDAY_VARIANTS_A).replace("Wellness Wednesday", ev)
            out.append({"instruction": q2, "output": sprinkle(a2)})
    return out


def dining_variations() -> list[dict]:
    out = []
    for spot in DINING:
        qs = [
            f"is {spot} good?",
            f"what are {spot} hours?",
            f"does {spot} have vegan options?",
            f"can I mobile order at {spot}?",
        ]
        ans = [
            f"people find their go-tos—menus rotate, so check before you roll to {spot}.",
            f"hours shift during breaks—{spot} posts updates online.",
            f"there’s usually a plant-based option—{spot} labels pretty well.",
            f"if mobile order’s live, do it—saves you 15 minutes at {spot}.",
        ]
        for i in range(4):
            out.append({"instruction": qs[i], "output": sprinkle(ans[i])})
    return out


def athletics_variations() -> list[dict]:
    out = []
    qs = [x for x, _ in ATHLETICS_QA]
    ans = [y for _, y in ATHLETICS_QA]
    for i in range(240):
        q = random.choice(qs)
        a = random.choice(ans)
        out.append({"instruction": q, "output": sprinkle(a)})
    return out


def synthesize(target_count: int = 5000) -> list[dict]:
    data: list[dict] = []
    # Seed with targeted creative augmentations
    data.extend(distance_variations())
    data.extend(service_variations())
    data.extend(generic_variations(ACADEMICS_QA))
    data.extend(generic_variations(REC_QA))
    data.extend(generic_variations(LIBRARY_QA))
    data.extend(generic_variations(SAFETY_QA))
    data.extend(generic_variations(AID_QA))
    data.extend(generic_variations(CAREER_QA))
    data.extend(generic_variations(ABROAD_QA))
    data.extend(generic_variations(IT_QA))
    data.extend(generic_variations(WELLNESS_QA))
    data.extend(generic_variations(DSS_QA))
    data.extend(generic_variations(OISS_QA))
    data.extend(generic_variations(PARKING_QA))
    data.extend(generic_variations(DINING_QA))
    data.extend(generic_variations(SOCIAL_QA))
    data.extend(generic_variations(CAMPUS_TIPS_QA))
    data.extend(events_variations())
    data.extend(dining_variations())

    # Additional chatter synthesis with LMU-flavored prompts
    chatter_topics = [
        ("parking at LMU", "parking fills up—permits don’t guarantee spots, time it right."),
        ("RSVPs for events", "event pages or club links—free food events cap fast, no cap."),
        ("sunset spots on campus", "the bluff, easy pick—bring a hoodie, it gets breezy."),
        ("best times for the gym", "avoid 5–8pm—mornings are wide open if you can wake up."),
        ("printing before class", "upload ahead and release at the nearest printer—don’t line up last minute."),
        ("meal plan hacks", "mix swipes and dining dollars, and check specials at Lair Marketplace."),
        ("finding quiet study corners", "top floors of Hannon and tucked U-Hall spots are underrated."),
        ("intramurals signups", "they open fast—set an alarm and snag your team’s slot."),
        ("career fair prep", "one-page resume, elevator pitch, and a follow-up email—works wonders."),
        ("study abroad timing", "do it sophomore/junior year so sequences still line up."),
    ]
    for topic, base in chatter_topics:
        for _ in range(60):
            q = random.choice(SLANG_Q).replace("{x}", topic)
            data.append({"instruction": q, "output": sprinkle(base)})

    # Top up to target_count with randomized blends
    blend_qas = (
        ACADEMICS_QA + REC_QA + ATHLETICS_QA + LIBRARY_QA + SAFETY_QA +
        AID_QA + CAREER_QA + ABROAD_QA + IT_QA + WELLNESS_QA + DSS_QA +
        OISS_QA + PARKING_QA + DINING_QA + SOCIAL_QA + CAMPUS_TIPS_QA
    )

    buildings_local = BUILDINGS[:]
    while len(data) < target_count:
        # 40% campus-life blend, 40% LMU-specific, 20% events/dining
        r = random.random()
        if r < 0.4:
            q, a = random.choice(blend_qas)
            data.append({"instruction": random.choice([
                q,
                q.replace("?", " (LMU)?"),
                q.replace("?", "—worth it?"),
            ]), "output": sprinkle(a)})
        elif r < 0.8:
            a, b = random.sample(buildings_local, 2)
            mins = random.randint(4, 12)
            q = random.choice([
                f"how far is it from {a} to {b}?",
                f"{a} → {b} walk time?",
                f"could I scooter from {a} to {b}?",
                f"is {a} to {b} a hike?",
            ])
            ans = random.choice([
                f"{a} to {b} is ~{mins} minutes on foot—scooters make it breeze by.",
                f"call it {mins} min walking; add 1–2 if crowds hit between classes.",
                f"not bad—{mins}ish unless you stop at the bluff.",
            ])
            data.append({"instruction": q, "output": sprinkle(ans)})
        else:
            if random.random() < 0.5:
                ev = random.choice(EVENTS)
                q = random.choice(WELLNESS_WEDNESDAY_VARIANTS_Q).replace("Wellness Wednesday", ev)
                a = random.choice(WELLNESS_WEDNESDAY_VARIANTS_A).replace("Wellness Wednesday", ev)
                data.append({"instruction": q, "output": sprinkle(a)})
            else:
                spot = random.choice(DINING)
                q = random.choice([
                    f"is {spot} open late?",
                    f"is {spot} worth it?",
                    f"does {spot} have vegan options?",
                    f"what are {spot} hours?",
                ])
                a = random.choice([
                    f"hours shift—check before you go; {spot} posts updates.",
                    f"menus rotate; people find go-tos—{spot} is solid when not slammed.",
                    f"usually a plant-based option; labels help at {spot}.",
                ])
                data.append({"instruction": q, "output": sprinkle(a)})

    random.shuffle(data)
    return data


def main():
    path = Path("/workspace/lmu_training_data.json")
    data = synthesize(target_count=6000)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(data)} examples to {path}")


if __name__ == "__main__":
    main()
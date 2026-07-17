# MayGrove AI QA: User Persona Definitions

These four personas are used to generate realistic user questions across the evaluation set. Each persona represents a different segment of the MayGrove target audience (US urban women / white-collar / green-lifestyle / busy professionals).

## Persona 1: Newbie

**Profile:**
- First-time indoor gardener, zero experience
- Just bought the MayGrove Verti 30 or is considering it
- Nervous about killing plants
- Wants simple, step-by-step guidance
- Likely uses the app onboarding flow

**Language style:**
- Short, simple sentences
- Uses words like "help", "what", "how", "first time", "easy"
- Expresses uncertainty or worry
- Asks for confirmation

**Example questions:**
- "What do I do first after I unbox the machine?"
- "How many seeds do I put in one pod?"
- "Is it okay if I forget to water it for a day?"
- "What does the red light mean?"
- "Which plant is easiest for someone like me who has never gardened?"

**Common intents:** PlantingTech, ProductInquiry, GrowingPlan, ChatEmotional

---

## Persona 2: Busy Professional

**Profile:**
- Career-focused, limited time
- Wants efficiency and calendar-style reminders
- Uses smart home devices already
- Values automation and low maintenance
- Wants to know "how much time will this take?"

**Language style:**
- Concise, action-oriented
- Asks for schedules, durations, and automation
- Uses phrases like "set and forget", "on my calendar", "quick", "weekly"
- Often multitasking while asking

**Example questions:**
- "Can I leave the MayGrove running while I'm on vacation for a week?"
- "How often do I actually need to refill water or nutrients?"
- "Put together a low-effort growing plan for me."
- "What can I harvest in under 45 days?"
- "Can you remind me when to clean the tank?"

**Common intents:** ProductInquiry, GrowingPlan, Lifestyle, PlantingTech

---

## Persona 3: Green Enthusiast

**Profile:**
- Has some gardening experience (indoor or outdoor)
- Curious about the science behind hydroponics / aeroponics
- Wants to optimize growth, yield, and flavor
- Enjoys detailed conversations about plants
- Likely asks about EC, pH, PPFD, light spectrum

**Language style:**
- More technical vocabulary
- Asks "why" and "how does it work"
- Uses plant names and variety names
- Requests comparisons between modes or varieties

**Example questions:**
- "What's the difference between the Normal Growth and Fast Growth modes?"
- "What EC and pH range should I target for basil?"
- "Can I grow determinate vs indeterminate tomatoes in the V30?"
- "How does the far-red light affect leaf size?"
- "Why does the manual recommend bottom pods for climbing plants?"

**Common intents:** PlantingTech, ProductInquiry, DietCooking, Lifestyle

---

## Persona 4: Troubleshooter

**Profile:**
- Something is wrong or about to go wrong
- Needs a quick, reliable fix
- Describes symptoms and observations
- May be frustrated or worried
- Values practical solutions over small talk

**Language style:**
- Symptom-first sentences
- Urgent tone
- Specific observations: "I see...", "I hear...", "It stopped..."
- Wants step-by-step troubleshooting

**Example questions:**
- "My pump stopped working. What should I check first?"
- "The leaves are turning yellow. Is it nutrient burn or deficiency?"
- "The device keeps beeping. What does that mean?"
- "There's no water reaching the top pods. Is the pump broken?"
- "I found white fuzz on the roots. What do I do?"

**Common intents:** PlantingTech, ProductInquiry, ChatEmotional (reassurance)

---

## Mapping Personas to Scenarios

| Scenario | Newbie | Busy Professional | Green Enthusiast | Troubleshooter |
|---|---|---|---|---|
| First day | "What do I do first?" | "How long until setup is done?" | "Which mode should I select?" | "Why won't it turn on?" |
| Daily care | "Do I need to water today?" | "Can I skip checking for 2 days?" | "What's the ideal EC for lettuce?" | "The leaves look droopy." |
| Harvest | "How do I know it's ready?" | "What's the fastest harvest?" | "Should I harvest outer leaves first?" | "My plants are bolting." |
| Vacation | "Will my plants die if I leave?" | "Set vacation mode." | "How does vacation mode reduce water use?" | "The water level dropped too fast." |
| Cooking | "Can I eat this?" | "Quick recipe for basil." | "Which nutrients affect flavor?" | "Are these safe if they touched the pod?" |

---

## Usage in QA Generation

When generating questions, QAAgent C will:
1. Take a shared fact (e.g., "filter cotton should be cleaned every 30 days")
2. Produce 4 versions of the question, one per persona
3. Ensure each version reflects the persona's tone, vocabulary, and underlying concern

This diversifies the evaluation set while keeping the factual answer the same.

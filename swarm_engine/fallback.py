# swarm_engine/fallback.py
# ─────────────────────────────────────────────────────────────────────────────
# Static dummy output for when the LLM is unavailable (rate limits, API down).
# Represents a full 5-iteration run with 10 virtualised micro-agents, each
# with a distinct personality from agents/personalities.py.
#
# Used by main.py when swarm execution raises any exception.
# ─────────────────────────────────────────────────────────────────────────────

PROBLEM = "AI project idea in the field of healthcare"

# 10 agents drawn from personalities.py (one per virtual copy of the model)
_AGENTS = [
    {"id": 1,  "style": "analytical"},
    {"id": 2,  "style": "creative"},
    {"id": 3,  "style": "pragmatic"},
    {"id": 4,  "style": "critical"},
    {"id": 5,  "style": "holistic"},
    {"id": 6,  "style": "minimalist"},
    {"id": 7,  "style": "ambitious"},
    {"id": 8,  "style": "empathetic"},
    {"id": 9,  "style": "systematic"},
    {"id": 10, "style": "divergent"},
]

# ─────────────────────────────────────────────────────────────────────────────
# Pre-generated ideas — 10 per iteration, 5 iterations = 50 ideas total
# Each idea shows the agent's distinct thinking style through content + reason
# ─────────────────────────────────────────────────────────────────────────────

DUMMY_ITERATIONS = [
    # ── ITERATION 1 — Fresh generation (all agents think independently) ──────
    {
        "problem":   PROBLEM,
        "iteration": 1,
        "ideas": [
            {
                "agent_id":    1,
                "agent_style": "analytical",
                "content":     "Build an AI diagnostic platform that cross-references patient lab results, imaging data, and EHR history to surface statistically significant anomalies missed by individual clinicians.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Pattern recognition across multi-modal structured data is where AI outperforms human review most measurably.",
                "score":       7.8,
                "votes":       0,
            },
            {
                "agent_id":    2,
                "agent_style": "creative",
                "content":     "Create a 'Digital Twin' of each patient — a running simulation of their physiology trained on their personal health history — so doctors can test treatment scenarios before applying them in real life.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Simulating outcomes before intervention eliminates harm and accelerates confident decision-making.",
                "score":       9.1,
                "votes":       0,
            },
            {
                "agent_id":    3,
                "agent_style": "pragmatic",
                "content":     "Develop an AI-powered medication adherence app that sends adaptive reminders calibrated to each patient's schedule, lifestyle, and past missed-dose patterns.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Medication non-adherence costs the US healthcare system $300B/year — a targeted nudge system delivers immediate ROI.",
                "score":       7.2,
                "votes":       0,
            },
            {
                "agent_id":    4,
                "agent_style": "critical",
                "content":     "Build an AI-powered second-opinion system for radiologists that flags diagnostic images with a confidence score and highlights the specific regions driving the AI's assessment.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Radiology error rates are 3-5%; an explainable AI layer reduces liability and increases catch rate without replacing the clinician.",
                "score":       8.4,
                "votes":       0,
            },
            {
                "agent_id":    5,
                "agent_style": "holistic",
                "content":     "Create an integrated mental + physical health AI that correlates wearable sensor data (sleep, HRV, activity) with self-reported mood to detect burnout and depression before clinical thresholds are crossed.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Mental and physical health are inseparable; treating them as one data stream reveals earlier warning signals.",
                "score":       8.7,
                "votes":       0,
            },
            {
                "agent_id":    6,
                "agent_style": "minimalist",
                "content":     "Build a single-purpose AI triage chatbot that takes five symptom inputs and outputs a ranked list of likely conditions with urgency level, integrated directly into hospital intake forms.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Reducing ER wait times by even 15 minutes improves patient outcomes — simplicity and speed matter more than feature richness here.",
                "score":       7.0,
                "votes":       0,
            },
            {
                "agent_id":    7,
                "agent_style": "ambitious",
                "content":     "Launch a federated learning network across 500 hospitals worldwide that trains a shared oncology AI model on local patient data without any data ever leaving the hospital, achieving scale without privacy violation.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Federated learning is the only path to global-scale medical AI without breaking HIPAA or GDPR — this is the moonshot worth building.",
                "score":       9.3,
                "votes":       0,
            },
            {
                "agent_id":    8,
                "agent_style": "empathetic",
                "content":     "Develop an AI mental health companion for elderly patients in assisted living that learns their life stories, provides conversational support, and alerts care staff to signs of cognitive decline.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Loneliness is the #1 health risk for elderly patients — an AI companion that truly listens addresses root cause, not symptom.",
                "score":       8.1,
                "votes":       0,
            },
            {
                "agent_id":    9,
                "agent_style": "systematic",
                "content":     "Build a clinical workflow automation AI that reads doctor notes, auto-populates insurance pre-authorisation forms, and tracks submission status, eliminating 4+ hours of admin per clinician per day.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Administrative burden is the top cause of physician burnout — removing paperwork AI is the highest leverage operational improvement available.",
                "score":       7.6,
                "votes":       0,
            },
            {
                "agent_id":    10,
                "agent_style": "divergent",
                "content":     "Use AI to redesign how clinical trials recruit patients — scrape EHR networks in real time to find trial-eligible patients and automatically notify their physicians, cutting recruitment timelines from 3 years to 6 months.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "90% of clinical trials fail due to poor recruitment; AI matching eliminates the bottleneck that slows every drug to market.",
                "score":       8.9,
                "votes":       0,
            },
        ],
    },

    # ── ITERATION 2 — Agents refine and combine the best ideas ──────────────
    {
        "problem":   PROBLEM,
        "iteration": 2,
        "ideas": [
            {
                "agent_id":    1,
                "agent_style": "analytical",
                "content":     "Extend the AI diagnostic platform to include temporal analysis — tracking how a patient's biomarkers drift over time to predict organ failure 30–90 days before clinical onset.",
                "parent_ids":  [1],
                "action_type": "refine",
                "reason":      "Point-in-time diagnostics miss trajectory; longitudinal pattern drift is the most predictive signal available in EHR data.",
                "score":       8.5,
                "votes":       0,
            },
            {
                "agent_id":    2,
                "agent_style": "creative",
                "content":     "Merge the Digital Twin and the federated learning network: each hospital's Digital Twin models train collaboratively via federated learning, producing globally-accurate patient simulations with zero data sharing.",
                "parent_ids":  [2, 7],
                "action_type": "combine",
                "reason":      "The two strongest ideas are architecturally compatible — combining them multiplies both accuracy and privacy simultaneously.",
                "score":       9.5,
                "votes":       0,
            },
            {
                "agent_id":    3,
                "agent_style": "pragmatic",
                "content":     "Add pharmacy integration to the medication adherence app so that when a patient misses a dose pattern consistently, the system automatically contacts their pharmacist to arrange blister-pack repackaging.",
                "parent_ids":  [3],
                "action_type": "refine",
                "reason":      "Pharmacist intervention is the most evidence-backed adherence tool — the AI identifies who needs it and removes the referral friction.",
                "score":       7.9,
                "votes":       0,
            },
            {
                "agent_id":    4,
                "agent_style": "critical",
                "content":     "The Digital Twin idea is exciting but needs a validation framework — build an AI that continuously backtests each patient's Digital Twin against their actual outcomes to score its predictive accuracy and flag when it needs retraining.",
                "parent_ids":  [2],
                "action_type": "refine",
                "reason":      "A Digital Twin without measurable predictive validity is just an expensive dashboard; this adds the scientific rigour it requires.",
                "score":       8.8,
                "votes":       0,
            },
            {
                "agent_id":    5,
                "agent_style": "holistic",
                "content":     "Combine the mental health AI and the Digital Twin: the digital twin tracks physiological state while the mental health layer tracks emotional state, producing a unified well-being score surfaced to the care team.",
                "parent_ids":  [5, 2],
                "action_type": "combine",
                "reason":      "Unifying physical simulation with emotional tracking creates a whole-person health model that neither idea achieves alone.",
                "score":       9.0,
                "votes":       0,
            },
            {
                "agent_id":    6,
                "agent_style": "minimalist",
                "content":     "Strip the triage chatbot down to a voice interface — patients describe symptoms out loud, the AI transcribes and analyses, and outputs urgency in 10 seconds. No typing, no friction.",
                "parent_ids":  [6],
                "action_type": "refine",
                "reason":      "Typing is a barrier for elderly or distressed patients; voice removes the last friction point in self-triage.",
                "score":       7.4,
                "votes":       0,
            },
            {
                "agent_id":    7,
                "agent_style": "ambitious",
                "content":     "Expand the federated oncology network to include genomic sequencing data alongside imaging, enabling the first truly multi-modal global cancer AI trained on 10 million patients without any patient record leaving its origin hospital.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "Imaging alone misses 40% of oncology signal present in genomics — multi-modal fusion at federated scale is the path to superhuman cancer detection.",
                "score":       9.4,
                "votes":       0,
            },
            {
                "agent_id":    8,
                "agent_style": "empathetic",
                "content":     "Give the elderly AI companion a 'family bridge' feature — it generates a weekly natural-language summary of conversation themes, mood trends, and health flags, sent directly to the patient's family with their consent.",
                "parent_ids":  [8],
                "action_type": "refine",
                "reason":      "Family involvement is the second-most effective intervention for elderly well-being — the AI makes it effortless and data-informed.",
                "score":       8.3,
                "votes":       0,
            },
            {
                "agent_id":    9,
                "agent_style": "systematic",
                "content":     "Extend the workflow automation AI to generate the insurance denial appeal letter automatically when a pre-auth is rejected, using the clinical notes and evidence literature as supporting material.",
                "parent_ids":  [9],
                "action_type": "refine",
                "reason":      "80% of denied claims are successfully appealed when clinical evidence is cited — automating this recovers significant revenue per physician per year.",
                "score":       8.0,
                "votes":       0,
            },
            {
                "agent_id":    10,
                "agent_style": "divergent",
                "content":     "Flip the clinical trial recruitment model: instead of finding patients for trials, build an AI that tells each patient which active trials they qualify for at the moment of diagnosis, embedded inside patient-facing apps.",
                "parent_ids":  [10],
                "action_type": "refine",
                "reason":      "Patient-initiated trial discovery is faster and more empowering than physician-mediated referral — flipping the direction unlocks latent interest.",
                "score":       9.1,
                "votes":       0,
            },
        ],
    },

    # ── ITERATION 3 — Survivors evolve; weakest replaced by new angles ───────
    {
        "problem":   PROBLEM,
        "iteration": 3,
        "ideas": [
            {
                "agent_id":    1,
                "agent_style": "analytical",
                "content":     "Layer a causal inference engine on top of the longitudinal biomarker tracker to distinguish correlation from causation in patient deterioration, enabling interventions that address root cause rather than downstream signals.",
                "parent_ids":  [1],
                "action_type": "refine",
                "reason":      "Causal graphs eliminate spurious correlations that corrupt predictive models and lead to wrong clinical actions.",
                "score":       9.0,
                "votes":       0,
            },
            {
                "agent_id":    2,
                "agent_style": "creative",
                "content":     "Build a 'Swarm Diagnosis' feature where 100 virtual specialist agents (cardiologist, neurologist, oncologist…) each independently assess the same patient case and vote, surfacing rare condition hypotheses no single specialist would flag.",
                "parent_ids":  [2],
                "action_type": "refine",
                "reason":      "Rare diseases are missed because no single specialist covers all the signal — a virtualised multi-specialist consensus changes the odds.",
                "score":       9.6,
                "votes":       0,
            },
            {
                "agent_id":    3,
                "agent_style": "pragmatic",
                "content":     "Partner the adherence app with pharmacy chains (CVS, Walgreens) via API so refill delays are detected automatically and the system negotiates 90-day supplies on the patient's behalf.",
                "parent_ids":  [3],
                "action_type": "refine",
                "reason":      "Half of adherence failures are logistics, not motivation — automating refill management solves the structural problem.",
                "score":       8.0,
                "votes":       0,
            },
            {
                "agent_id":    4,
                "agent_style": "critical",
                "content":     "Apply the Digital Twin validation framework to the federated oncology model — each hospital's local model is backtested against ground-truth outcomes before its weights are contributed to the global aggregate.",
                "parent_ids":  [4, 7],
                "action_type": "combine",
                "reason":      "Federated learning is only as good as its worst contributor — local validation gates prevent poisoning the global model.",
                "score":       9.2,
                "votes":       0,
            },
            {
                "agent_id":    5,
                "agent_style": "holistic",
                "content":     "Add a social determinants of health layer to the unified well-being score — pulling in ZIP-code-level data on food access, air quality, and income to contextualise why a patient's health trajectory looks the way it does.",
                "parent_ids":  [5],
                "action_type": "refine",
                "reason":      "80% of health outcomes are determined by social factors; ignoring them makes any AI model systematically biased toward privileged populations.",
                "score":       8.9,
                "votes":       0,
            },
            {
                "agent_id":    6,
                "agent_style": "minimalist",
                "content":     "Compress the entire value proposition of the federated network into a single open-source SDK hospitals can install in one command, removing the engineering barrier that stops adoption.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "The best privacy-preserving AI system is the one that actually gets deployed — installation friction kills adoption more than any technical gap.",
                "score":       7.7,
                "votes":       0,
            },
            {
                "agent_id":    7,
                "agent_style": "ambitious",
                "content":     "Build a real-time pandemic early-warning system that aggregates anonymised symptom signals from the federated hospital network and flags novel outbreak clusters to health authorities within 48 hours of emergence.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "COVID-19 spread for 6 weeks before detection — a federated signal aggregator makes that impossible for future pathogens.",
                "score":       9.7,
                "votes":       0,
            },
            {
                "agent_id":    8,
                "agent_style": "empathetic",
                "content":     "Integrate the elderly AI companion with the social determinants layer — if the companion detects food insecurity signals in conversation, it automatically contacts local meal-delivery services on the patient's behalf.",
                "parent_ids":  [8, 5],
                "action_type": "combine",
                "reason":      "Conversation data reveals unmet social needs that clinical records never capture — the AI companion is the ideal social determinants sensor.",
                "score":       8.6,
                "votes":       0,
            },
            {
                "agent_id":    9,
                "agent_style": "systematic",
                "content":     "Build an AI that maps every step of the insurance claims lifecycle and identifies the exact documentation gap that caused each denial, then generates a corrected claim automatically for resubmission.",
                "parent_ids":  [9],
                "action_type": "refine",
                "reason":      "Systematic root-cause classification of denials enables structural fixes, not just one-off appeals.",
                "score":       8.3,
                "votes":       0,
            },
            {
                "agent_id":    10,
                "agent_style": "divergent",
                "content":     "Create an AI marketplace where patients can 'donate' their anonymised health data to specific research causes in exchange for personalised health insights — turning data altruism into a viable research funding model.",
                "parent_ids":  [],
                "action_type": "generate",
                "reason":      "Patient data is the scarcest resource in medical AI; aligning patient incentives with research needs unlocks supply no regulation currently permits.",
                "score":       9.0,
                "votes":       0,
            },
        ],
    },

    # ── ITERATION 4 — Elite agents push ideas to production-ready depth ──────
    {
        "problem":   PROBLEM,
        "iteration": 4,
        "ideas": [
            {
                "agent_id":    1,
                "agent_style": "analytical",
                "content":     "Publish the causal inference engine as a peer-reviewed open benchmark, tested on 10 real-world ICU datasets, so hospitals can validate it before deployment — making regulatory approval tractable for the first time.",
                "parent_ids":  [1],
                "action_type": "refine",
                "reason":      "Regulators approve AI they can independently evaluate; an open benchmark is the fastest path through FDA's Software as a Medical Device framework.",
                "score":       8.8,
                "votes":       0,
            },
            {
                "agent_id":    2,
                "agent_style": "creative",
                "content":     "Give the Swarm Diagnosis feature a 'minority report' mode — it surfaces the dissenting agents' hypotheses alongside the consensus, so rare-disease signals are never silenced by majority vote.",
                "parent_ids":  [2],
                "action_type": "refine",
                "reason":      "Medical consensus kills rare-disease diagnosis; preserving dissent as a first-class output changes the epistemology of AI-assisted medicine.",
                "score":       9.4,
                "votes":       0,
            },
            {
                "agent_id":    3,
                "agent_style": "pragmatic",
                "content":     "Launch the adherence platform as a white-label SaaS sold directly to pharmaceutical companies whose drugs have known adherence problems, turning patient compliance into a pharma revenue lever.",
                "parent_ids":  [3],
                "action_type": "refine",
                "reason":      "Pharma companies lose $637B/year to non-adherence; they will pay handsomely for a solution — this is the GTM that makes the product self-funding.",
                "score":       8.5,
                "votes":       0,
            },
            {
                "agent_id":    4,
                "agent_style": "critical",
                "content":     "Apply the Swarm Diagnosis consensus model to the claims denial root-cause classifier — 50 virtual insurance expert agents each score the clinical documentation gap independently and vote on the correction strategy.",
                "parent_ids":  [2, 9],
                "action_type": "combine",
                "reason":      "Insurance coding is as complex as clinical diagnosis — the same consensus architecture that catches rare diseases can catch rare billing errors.",
                "score":       8.7,
                "votes":       0,
            },
            {
                "agent_id":    5,
                "agent_style": "holistic",
                "content":     "Build a 'Community Health Navigator' that aggregates Digital Twin data at ZIP-code level to identify which interventions (food, housing, mental health) would produce the highest well-being ROI for that community.",
                "parent_ids":  [5, 2],
                "action_type": "combine",
                "reason":      "Individual health AI optimises one patient; community-level aggregation allows public health systems to allocate resources where they matter most.",
                "score":       9.1,
                "votes":       0,
            },
            {
                "agent_id":    6,
                "agent_style": "minimalist",
                "content":     "Reduce the pandemic early-warning system to a single daily risk score per city, delivered to public health dashboards as a REST API endpoint requiring zero infrastructure from city governments.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "A single interpretable metric with no setup friction gets adopted; 50-metric dashboards get ignored.",
                "score":       7.9,
                "votes":       0,
            },
            {
                "agent_id":    7,
                "agent_style": "ambitious",
                "content":     "Negotiate a global treaty-level data-sharing agreement between the top 20 health ministries using the federated privacy framework as the legal and technical foundation, creating the first interoperable global health AI.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "Technology alone cannot solve global health — embedding the federated architecture in international health law makes it structurally permanent.",
                "score":       9.5,
                "votes":       0,
            },
            {
                "agent_id":    8,
                "agent_style": "empathetic",
                "content":     "Train the elderly AI companion on end-of-life care literature so it can facilitate gentle conversations about advance care planning, surfacing patient wishes to both family and care team in a structured, legally usable format.",
                "parent_ids":  [8],
                "action_type": "refine",
                "reason":      "80% of people want to die at home; 60% do so in a hospital — this is a palliative care failure caused by unrecorded preferences.",
                "score":       9.2,
                "votes":       0,
            },
            {
                "agent_id":    9,
                "agent_style": "systematic",
                "content":     "Integrate the claims AI with hospital ERP systems so every denied-claim correction and resubmission is tracked end-to-end in a compliance audit trail, making it defensible in regulatory review.",
                "parent_ids":  [9],
                "action_type": "refine",
                "reason":      "Healthcare AI that cannot produce a compliance audit trail will not survive procurement — this makes the system enterprise-grade by design.",
                "score":       8.2,
                "votes":       0,
            },
            {
                "agent_id":    10,
                "agent_style": "divergent",
                "content":     "Design the patient data marketplace as a DAO (decentralised autonomous organisation) where governance and revenue are controlled by contributing patients — making them shareholders, not just donors.",
                "parent_ids":  [10],
                "action_type": "refine",
                "reason":      "DAO governance is the only model that aligns patient long-term interests with research sustainability — the first patient-owned medical AI dataset.",
                "score":       8.8,
                "votes":       0,
            },
        ],
    },

    # ── ITERATION 5 — Synthesis: best survivors converge on the final vision ──
    {
        "problem":   PROBLEM,
        "iteration": 5,
        "ideas": [
            {
                "agent_id":    1,
                "agent_style": "analytical",
                "content":     "Combine the causal inference engine with the community health navigator to not only explain why a community's health is declining but to prescribe the minimum intervention set with maximum statistical effect.",
                "parent_ids":  [1, 5],
                "action_type": "combine",
                "reason":      "Causal inference tells you what to change; the community navigator tells you where — combining them produces optimal resource allocation under uncertainty.",
                "score":       9.3,
                "votes":       0,
            },
            {
                "agent_id":    2,
                "agent_style": "creative",
                "content":     "Publish the Swarm Diagnosis architecture as an open protocol so any hospital can run their own specialist swarm — virtualising the world's medical expertise and making rare-disease diagnosis accessible in rural clinics globally.",
                "parent_ids":  [2],
                "action_type": "refine",
                "reason":      "Proprietary AI concentrates expertise in rich countries; an open protocol democratises it — this is the version that actually saves the most lives.",
                "score":       9.8,
                "votes":       0,
            },
            {
                "agent_id":    3,
                "agent_style": "pragmatic",
                "content":     "Build a 90-day go-to-market plan for the adherence SaaS: sign three pharma pilot contracts in Q1, instrument the adherence improvement lift, and use the verified ROI data to close the next ten deals without a sales team.",
                "parent_ids":  [3],
                "action_type": "refine",
                "reason":      "The product is ready; what it needs is a proof-of-ROI loop that makes every new customer a reference case for the next.",
                "score":       8.2,
                "votes":       0,
            },
            {
                "agent_id":    4,
                "agent_style": "critical",
                "content":     "Mandate a bias audit requirement in the federated oncology model — before any hospital's weights are merged, an independent fairness classifier checks that the local model's error rates are equitable across race, age, and sex.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "Federated learning can federate bias just as efficiently as it federates accuracy — this gate prevents systemic harm at global scale.",
                "score":       9.5,
                "votes":       0,
            },
            {
                "agent_id":    5,
                "agent_style": "holistic",
                "content":     "Integrate every system built in this swarm — Digital Twin, federated network, well-being score, social determinants, and Swarm Diagnosis — into a unified API layer called the 'Human Health Operating System'.",
                "parent_ids":  [2, 5, 7, 8],
                "action_type": "combine",
                "reason":      "Each component is powerful alone; as a unified OS they become infrastructure — the same way TCP/IP made the internet, this makes AI-native healthcare inevitable.",
                "score":       9.9,
                "votes":       0,
            },
            {
                "agent_id":    6,
                "agent_style": "minimalist",
                "content":     "Expose the Human Health Operating System as a single developer API with 10 endpoints and clear documentation so every health-tech startup builds on top of it instead of reinventing the data layer.",
                "parent_ids":  [5],
                "action_type": "refine",
                "reason":      "Platform wins come from simplicity of integration — 10 well-designed endpoints create more downstream innovation than 500 features.",
                "score":       8.6,
                "votes":       0,
            },
            {
                "agent_id":    7,
                "agent_style": "ambitious",
                "content":     "File for WHO recognition of the federated health AI protocol as the global standard for cross-border medical data collaboration, embedding the privacy and bias frameworks into international health law.",
                "parent_ids":  [7],
                "action_type": "refine",
                "reason":      "WHO standards become mandatory — this turns a technical architecture into a permanent global institution.",
                "score":       9.6,
                "votes":       0,
            },
            {
                "agent_id":    8,
                "agent_style": "empathetic",
                "content":     "Make the Human Health OS patient-controlled by default — each patient holds a cryptographic key to their own data and must consent before any agent, hospital, or researcher can access it.",
                "parent_ids":  [5, 10],
                "action_type": "combine",
                "reason":      "Data sovereignty is the missing ethical layer; without it, the Human Health OS is infrastructure for surveillance, not care.",
                "score":       9.4,
                "votes":       0,
            },
            {
                "agent_id":    9,
                "agent_style": "systematic",
                "content":     "Define a certification programme for hospitals to become 'Human Health OS nodes' — with a 12-month implementation checklist, compliance audit, and continuous monitoring SLA baked into the accreditation.",
                "parent_ids":  [9, 5],
                "action_type": "combine",
                "reason":      "A certification standard turns adoption from a sales problem into a compliance requirement — every hospital that wants accreditation becomes a customer.",
                "score":       8.9,
                "votes":       0,
            },
            {
                "agent_id":    10,
                "agent_style": "divergent",
                "content":     "Position the Human Health OS as open-source infrastructure (MIT licence) funded by a $1B endowment from three philanthropies, making it structurally independent of any government or corporation forever.",
                "parent_ids":  [5, 10],
                "action_type": "combine",
                "reason":      "Health infrastructure controlled by private capital becomes rent-extraction; open-source endowment is the only governance model that keeps it neutral.",
                "score":       9.3,
                "votes":       0,
            },
        ],
    },
]

DUMMY_FINAL_OUTPUT = """\
HUMAN HEALTH OPERATING SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A unified, open, patient-controlled AI infrastructure layer for healthcare.

CORE COMPONENTS (evolved across 5 iterations by 10 virtual micro-agents):
  1. Digital Twin Engine       — per-patient physiology simulation
  2. Federated Learning Network — global model training with zero data transfer
  3. Swarm Diagnosis Protocol  — 100+ virtual specialists vote on each case
  4. Causal Inference Engine   — root-cause analysis of patient trajectories
  5. Well-being Score          — unified mental + physical + social health signal
  6. Adherence Platform        — adaptive medication nudge system
  7. Pandemic Sentinel         — real-time outbreak early-warning from federated signals
  8. Elderly Companion AI      — conversational care with family bridge and EOL planning
  9. Claims Automation AI      — pre-auth, denial, appeal — fully automated
  10. Patient Data DAO          — patients own, govern, and benefit from their data

GOVERNANCE:
  — Open-source (MIT licence), endowment-funded
  — WHO-recognised cross-border data protocol
  — Patient cryptographic data sovereignty by default
  — Mandatory bias audit before any model weight is federated

IMPACT ESTIMATE:
  — 3-5% diagnostic error reduction across participating hospitals
  — $300B medication adherence losses recovered
  — Rare disease detection improved in clinics with zero specialist access
  — Pandemic detection window reduced from 6+ weeks to 48 hours
"""

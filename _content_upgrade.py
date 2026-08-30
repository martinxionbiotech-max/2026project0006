#!/usr/bin/env python3
"""Content deepening: unique title/meta/hero/FAQ per tool page (seriouscalculator.com)."""
import json, re, os, html

# slug -> {title, meta, hero, faq:[{q,a},...]}
# 3 unique questions (what / how / who) + 2 honest shared questions (accuracy / free+privacy)
SHARED_ACCURACY = {
    "q": "Is the result accurate?",
    "a": "Results are model-based estimates using static demographic assumptions, not exact predictions. Treat them as directional guidance for self-reflection and entertainment."
}
SHARED_FREE = {
    "q": "Is it free and private?",
    "a": "Yes. Every calculator is free, requires no sign-up, and runs entirely in your browser — no inputs are stored or transmitted."
}

TOOLS = {
"age-gap-compatibility": {
    "title": "Age Gap Compatibility Calculator – How Much Age Difference Matters",
    "meta": "See how an age gap affects relationship compatibility. Free tool that scores age difference against lifestyle, values, and communication factors.",
    "hero": "Estimate how an age gap affects relationship compatibility with a 0–100% score.",
    "faq": [
        {"q": "What is the Age Gap Compatibility tool?", "a": "It estimates how much an age difference between two partners is likely to affect relationship compatibility, based on lifestyle, communication, and values alignment."},
        {"q": "How is the age gap score calculated?", "a": "The tool weighs the age gap together with your lifestyle-match, communication-match, and core-values inputs, then returns a country-adjusted 0–100% score."},
        {"q": "What is an acceptable age gap?", "a": "There is no universal answer — research on relationship satisfaction varies. This tool gives a directional compatibility estimate, not a rule."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"age-gap-compatibility-calculator": {
    "title": "Age Gap Compatibility Calculator – Free 0–100% Score",
    "meta": "Free age gap compatibility calculator. Score your relationship's age difference against lifestyle and values to get a 0–100% match estimate.",
    "hero": "Measure relationship alignment across an age gap with a 0–100% compatibility score.",
    "faq": [
        {"q": "What does this calculator do?", "a": "It scores how well two partners may align across an age gap, using age difference plus lifestyle, communication, and values inputs."},
        {"q": "How does the age gap affect the score?", "a": "Larger age gaps typically lower the baseline score, but strong lifestyle and values matches offset the difference."},
        {"q": "Who is this calculator for?", "a": "Anyone curious about how an age difference might influence relationship compatibility — for reflection and entertainment."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"are-your-standards-too-high": {
    "title": "Are Your Dating Standards Too High? – Free Reality Check",
    "meta": "Check whether your dating standards are realistic. Free tool that compares your filters against demographic data to show your matching pool.",
    "hero": "Find out whether your dating standards match demographic reality.",
    "faq": [
        {"q": "What does this tool tell me?", "a": "It compares your dating filters (age, height, income, education) against population data and estimates how many people actually match them."},
        {"q": "How do I know if my standards are too high?", "a": "If your filters shrink the matching pool to a very small percentage, the tool flags that your standards may be stricter than the available population."},
        {"q": "Who should use this test?", "a": "Anyone wanting a reality check on their dating criteria before investing time in the search."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"attraction-compatibility-calculator": {
    "title": "Attraction Compatibility Calculator – Free Match Score",
    "meta": "Measure physical and personality attraction compatibility. Free calculator that scores attraction factors into a 0–100% match estimate.",
    "hero": "Score physical and personality attraction into a single compatibility estimate.",
    "faq": [
        {"q": "What does the Attraction Compatibility Calculator measure?", "a": "It combines physical-attraction and personality-attraction inputs into a single 0–100% compatibility estimate."},
        {"q": "How is attraction scored?", "a": "You rate attraction factors, and the tool weights them into a country-adjusted score for two people."},
        {"q": "Is attraction the same as compatibility?", "a": "No — attraction is one component of compatibility. This tool focuses on the attraction dimension specifically."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"breakup-risk-calculator": {
    "title": "Breakup Risk Calculator – Assess Relationship Stability",
    "meta": "Estimate the likelihood of a breakup based on relationship factors. Free tool that scores conflict, communication, and commitment risk.",
    "hero": "Estimate relationship breakup risk from conflict, communication, and commitment signals.",
    "faq": [
        {"q": "What does the Breakup Risk Calculator do?", "a": "It estimates the likelihood of a breakup by scoring relationship factors such as conflict frequency, communication quality, and commitment level."},
        {"q": "What factors increase breakup risk?", "a": "Frequent conflict, poor communication, and low commitment typically raise the estimated risk score."},
        {"q": "Who should use this tool?", "a": "People wanting a directional read on relationship stability — for reflection, not as a prediction."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"commitment-probability-calculator": {
    "title": "Commitment Probability Calculator – Will It Get Serious?",
    "meta": "Estimate how likely a relationship is to become committed. Free tool scoring readiness, investment, and alignment factors.",
    "hero": "Estimate the probability that a relationship progresses to commitment.",
    "faq": [
        {"q": "What does the Commitment Probability Calculator estimate?", "a": "It estimates how likely a relationship is to progress toward commitment, based on readiness, investment, and alignment inputs."},
        {"q": "What factors drive commitment probability?", "a": "Emotional readiness, mutual investment, and value alignment are the main factors the tool weighs."},
        {"q": "Who should use this calculator?", "a": "Anyone evaluating whether a current relationship is trending toward seriousness."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"communication-compatibility-score": {
    "title": "Communication Compatibility Score – How Well Do You Talk?",
    "meta": "Score how well two people communicate in a relationship. Free tool rating listening, conflict style, and openness.",
    "hero": "Score relationship communication quality with a 0–100% compatibility estimate.",
    "faq": [
        {"q": "What does the Communication Compatibility Score measure?", "a": "It rates how well two partners communicate, covering listening, conflict-handling style, and openness."},
        {"q": "Why does communication compatibility matter?", "a": "Communication is consistently cited as a top predictor of relationship satisfaction, which is why this tool isolates it."},
        {"q": "How is the score calculated?", "a": "You rate communication behaviors for both partners, and the tool returns a country-adjusted 0–100% score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-age-gap-calculator": {
    "title": "Dating Age Gap Calculator – Is the Age Difference OK?",
    "meta": "Evaluate whether an age gap works in dating. Free calculator scoring age difference against lifestyle and values compatibility.",
    "hero": "Evaluate whether a dating age gap is compatible with your lifestyle and values.",
    "faq": [
        {"q": "What does the Dating Age Gap Calculator do?", "a": "It estimates whether an age difference between dating partners is compatible, weighting the gap against lifestyle and values."},
        {"q": "What age gap is too much?", "a": "There is no fixed limit — the tool shows how the gap affects a compatibility score rather than imposing a rule."},
        {"q": "Who is this for?", "a": "People dating with an age difference who want a directional compatibility read."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-luck-calculator": {
    "title": "Dating Luck Calculator – Fun Estimate of Your Dating Odds",
    "meta": "A lighthearted estimate of your dating luck based on demographics and filters. Free tool for entertainment and self-reflection.",
    "hero": "A playful estimate of your dating odds from demographic filters.",
    "faq": [
        {"q": "What is the Dating Luck Calculator?", "a": "It's a lighthearted tool that estimates your dating odds from demographic assumptions — meant for fun and reflection."},
        {"q": "How is 'luck' calculated?", "a": "The tool applies demographic filters to a population and returns a percentage representing your estimated odds."},
        {"q": "Should I take the result seriously?", "a": "No — treat it as entertainment. It is a model-based estimate, not a prediction of your actual dating outcomes."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-market-value-calculator": {
    "title": "Dating Market Value Calculator – Score Your Dating Position",
    "meta": "Evaluate your dating market value based on appearance, income, education, confidence, and social skills. Free percentile estimate.",
    "hero": "Estimate your dating market value percentile from appearance, income, and social factors.",
    "faq": [
        {"q": "What is dating market value?", "a": "It's a rough concept estimating how desirable you are in the dating pool, based on appearance, income, education, and social skills."},
        {"q": "How is my market value scored?", "a": "The tool weights your physical, status, and personality inputs and returns a country-adjusted percentile estimate."},
        {"q": "Is market value a real metric?", "a": "No — it is a simplified model for reflection, not a scientific measure of worth."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-pool-calculator": {
    "title": "Dating Pool Calculator – How Many People Match You?",
    "meta": "Estimate your realistic dating pool size based on age, height, income, and demographic filters. Free percentage estimate.",
    "hero": "Estimate how many people match your dating criteria as a percentage of the population.",
    "faq": [
        {"q": "What does the Dating Pool Calculator do?", "a": "It estimates the size of your realistic dating pool by applying age, height, income, and other filters to population data."},
        {"q": "Why is my dating pool so small?", "a": "Each strict filter compounds — age, height, income, and education combined can shrink the pool to a tiny percentage."},
        {"q": "How can I increase my dating pool?", "a": "Relaxing one or two filters typically expands the matching percentage significantly."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-pool-size-calculator": {
    "title": "Dating Pool Size Calculator – Estimate Your Matches",
    "meta": "Calculate your dating pool size from demographic filters. Free tool that shows how many people meet your criteria.",
    "hero": "Estimate how many people meet your dating criteria.",
    "faq": [
        {"q": "What does the Dating Pool Size Calculator estimate?", "a": "It estimates the number of people who match your filters within a population, expressed as a percentage."},
        {"q": "How is pool size calculated?", "a": "Demographic rates are applied to your age, height, income, and other filters, then compounded."},
        {"q": "Why do percentages drop so fast?", "a": "Filters multiply — a 20% age match times a 30% income match times a 40% height match already gives under 3%."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-reality-calculator": {
    "title": "Dating Reality Calculator – Full Dating Standards Report",
    "meta": "Get a full dating reality report: dating pool %, matching population, market value, and compatibility in one free tool.",
    "hero": "Get a full dating reality report combining pool size, market value, and compatibility.",
    "faq": [
        {"q": "What is the Dating Reality Calculator?", "a": "It's a comprehensive tool that combines dating pool size, market value, and compatibility into one reality report."},
        {"q": "What does the report include?", "a": "Dating pool percentage, matching population, market value percentile, and compatibility scores across dimensions."},
        {"q": "Who should use the full report?", "a": "Anyone wanting a single overview of how their standards translate into realistic odds."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-risk-calculator": {
    "title": "Dating Risk Calculator – Assess Your Dating Decisions",
    "meta": "Evaluate risk factors in your dating choices. Free tool scoring red flags, commitment risk, and compatibility risk.",
    "hero": "Estimate risk factors in your dating decisions.",
    "faq": [
        {"q": "What does the Dating Risk Calculator measure?", "a": "It scores risk factors in a dating scenario — red flags, commitment risk, and compatibility risk — into one estimate."},
        {"q": "What counts as high risk?", "a": "Multiple red flags, low commitment signals, and poor compatibility raise the estimated risk score."},
        {"q": "Is this relationship advice?", "a": "No — it is a model-based estimate for reflection, not a substitute for judgment or professional advice."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"dating-standards-calculator": {
    "title": "Dating Standards Calculator – Are Your Standards Realistic?",
    "meta": "Test whether your dating standards are realistic against demographic data. Free tool estimating your matching pool.",
    "hero": "Test whether your dating standards are realistic.",
    "faq": [
        {"q": "What does the Dating Standards Calculator do?", "a": "It compares your dating standards (age, height, income, education) against population data to estimate your matching pool."},
        {"q": "How do I know if my standards are realistic?", "a": "If your filters produce a reasonable matching percentage, they're likely realistic; a tiny percentage suggests otherwise."},
        {"q": "Should I lower my standards?", "a": "That's a personal decision — the tool only shows how strict your filters are relative to the population."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"emotional-availability-test": {
    "title": "Emotional Availability Test – How Ready Are You to Date?",
    "meta": "Assess your emotional availability for a relationship. Free self-assessment scoring readiness, openness, and commitment capacity.",
    "hero": "Assess how emotionally available you are for a relationship.",
    "faq": [
        {"q": "What does the Emotional Availability Test measure?", "a": "It scores your readiness for a relationship across emotional openness, past baggage, and commitment capacity."},
        {"q": "What does low emotional availability mean?", "a": "It suggests difficulty opening up or committing — often a signal to work on yourself before dating."},
        {"q": "Who should take this test?", "a": "Anyone wanting to understand their own readiness before pursuing a relationship."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"emotional-compatibility-calculator": {
    "title": "Emotional Compatibility Calculator – Free Match Score",
    "meta": "Score emotional compatibility between two partners. Free tool rating empathy, emotional expression, and support styles.",
    "hero": "Score emotional compatibility between two people.",
    "faq": [
        {"q": "What does the Emotional Compatibility Calculator measure?", "a": "It scores how well two partners align emotionally — empathy, expression style, and mutual support."},
        {"q": "How is emotional compatibility different from other scores?", "a": "It focuses purely on emotional connection rather than physical attraction or lifestyle factors."},
        {"q": "Why does emotional compatibility matter?", "a": "Emotional connection is a key driver of long-term relationship satisfaction."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"female-delusion-calculator": {
    "title": "Female Delusion Calculator – Reality Check for Dating Standards",
    "meta": "The viral Female Delusion Calculator tests whether relationship expectations match demographic reality. Free, no sign-up.",
    "hero": "Test whether your relationship expectations match demographic reality.",
    "faq": [
        {"q": "What is the Female Delusion Calculator?", "a": "It's a viral tool that tests whether your dating standards (age, height, income) match the actual available population."},
        {"q": "How does it work?", "a": "You set your preferences, and the tool applies demographic rates to show the percentage of men who meet them."},
        {"q": "Why are my results so low?", "a": "Combining strict filters — tall, high income, single — compounds quickly and shrinks the matching pool."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"financial-compatibility-calculator": {
    "title": "Financial Compatibility Calculator – Money & Relationships",
    "meta": "Score financial compatibility between partners. Free tool rating spending habits, saving goals, and money values.",
    "hero": "Score how well two partners align on money habits and values.",
    "faq": [
        {"q": "What does the Financial Compatibility Calculator measure?", "a": "It scores alignment on spending habits, saving goals, and money values between partners."},
        {"q": "Why does financial compatibility matter?", "a": "Money disagreements are a leading cause of relationship conflict, making financial alignment a strong predictor."},
        {"q": "How is the score calculated?", "a": "You rate each partner's money behaviors, and the tool returns a country-adjusted 0–100% score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"flirting-skill-score": {
    "title": "Flirting Skill Score – How Good Is Your Flirting?",
    "meta": "Rate your flirting skills with a free self-assessment. Score confidence, charm, and approach across common scenarios.",
    "hero": "Score your flirting skills with a quick self-assessment.",
    "faq": [
        {"q": "What does the Flirting Skill Score measure?", "a": "It rates your flirting ability across confidence, charm, and approach style in common scenarios."},
        {"q": "How is my flirting score calculated?", "a": "You self-rate flirting behaviors, and the tool weights them into a 0–100% score."},
        {"q": "Is this a real measure of charm?", "a": "No — it's a fun self-assessment for reflection, not a scientific measure."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"ghosting-probability-calculator": {
    "title": "Ghosting Probability Calculator – Will They Disappear?",
    "meta": "Estimate the likelihood of being ghosted based on relationship signals. Free tool scoring responsiveness and commitment.",
    "hero": "Estimate how likely a match is to ghost you.",
    "faq": [
        {"q": "What does the Ghosting Probability Calculator do?", "a": "It estimates the likelihood of being ghosted, based on responsiveness, commitment signals, and relationship stage."},
        {"q": "What signals raise ghosting risk?", "a": "Low responsiveness, vague plans, and early-stage connections typically raise the estimated probability."},
        {"q": "Should I trust the result?", "a": "No — it's a directional estimate for reflection, not a prediction of a specific person's behavior."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"how-many-people-find-you-attractive": {
    "title": "How Many People Find You Attractive? – Estimate",
    "meta": "Estimate how many people might find you attractive based on demographics. Free, lighthearted estimate for reflection.",
    "hero": "Estimate how many people might find you attractive.",
    "faq": [
        {"q": "What does this tool estimate?", "a": "It estimates how many people in a population might find you attractive, based on demographic and preference assumptions."},
        {"q": "How is attractiveness estimated?", "a": "The tool applies preference filters to population data and returns a percentage-based estimate."},
        {"q": "Is this an accurate measure?", "a": "No — attractiveness is subjective. Treat the result as a fun, directional estimate."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"ideal-partner-builder": {
    "title": "Ideal Partner Builder – Define What You Actually Want",
    "meta": "Build a realistic profile of your ideal partner. Free tool that ranks your priorities and estimates how common they are.",
    "hero": "Build a realistic ideal-partner profile and see how common it is.",
    "faq": [
        {"q": "What does the Ideal Partner Builder do?", "a": "It helps you define your ideal partner's traits and estimates how common that combination is in the population."},
        {"q": "Why does this matter?", "a": "Clarifying your priorities — and seeing which are rare — helps you set realistic expectations."},
        {"q": "How does it estimate rarity?", "a": "It applies your preferred traits to demographic data and returns a matching percentage."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"jealousy-test": {
    "title": "Jealousy Test – How Jealous Are You in Relationships?",
    "meta": "Assess your jealousy level with a free self-test. Score insecurity, trust, and possessiveness across common scenarios.",
    "hero": "Assess your jealousy level in relationships.",
    "faq": [
        {"q": "What does the Jealousy Test measure?", "a": "It scores your jealousy level across insecurity, trust, and possessiveness in relationship scenarios."},
        {"q": "What does a high jealousy score mean?", "a": "It suggests frequent insecurity or possessiveness, which can strain relationships."},
        {"q": "Is this a clinical assessment?", "a": "No — it's a self-reflection tool, not a diagnosis or professional evaluation."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"lifestyle-compatibility-calculator": {
    "title": "Lifestyle Compatibility Calculator – Do Your Lives Fit?",
    "meta": "Score lifestyle compatibility between partners. Free tool rating routines, social habits, and long-term goals.",
    "hero": "Score how well two lifestyles fit together.",
    "faq": [
        {"q": "What does the Lifestyle Compatibility Calculator measure?", "a": "It scores alignment on daily routines, social habits, and long-term goals between partners."},
        {"q": "Why does lifestyle matter more than attraction?", "a": "Day-to-day routines and goals shape long-term satisfaction more than initial attraction."},
        {"q": "How is the score calculated?", "a": "You rate lifestyle factors for both partners, and the tool returns a 0–100% alignment score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"long-distance-compatibility": {
    "title": "Long Distance Compatibility – Can It Work?",
    "meta": "Estimate whether a long-distance relationship can work. Free tool scoring communication, trust, and visit feasibility.",
    "hero": "Estimate whether a long-distance relationship is viable.",
    "faq": [
        {"q": "What does the Long Distance Compatibility tool do?", "a": "It estimates the viability of a long-distance relationship based on communication, trust, and visit feasibility."},
        {"q": "What makes long distance work?", "a": "Strong communication, mutual trust, and a realistic plan to close the distance are the key factors."},
        {"q": "Is long distance likely to fail?", "a": "Not necessarily — the tool shows directional factors, but outcomes vary widely by couple."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"love-compatibility-calculator": {
    "title": "Love Compatibility Calculator – Free Couples Score (0–100%)",
    "meta": "Score love compatibility between you and your partner. Free tool rating age gap, lifestyle, communication, and values.",
    "hero": "Measure relationship alignment with a country-adjusted 0–100% compatibility score.",
    "faq": [
        {"q": "What does the Love Compatibility Calculator do?", "a": "It scores overall relationship compatibility from age gap, lifestyle match, communication match, and core values."},
        {"q": "How is the love score calculated?", "a": "You rate age gap, lifestyle, communication, and values; the tool weights them into a 0–100% country-adjusted score."},
        {"q": "What is a good compatibility score?", "a": "Higher scores suggest better alignment, but the number is directional — real compatibility involves many unmeasured factors."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"loyalty-test": {
    "title": "Loyalty Test – How Loyal Are You in Relationships?",
    "meta": "Assess relationship loyalty with a free self-test. Score commitment, honesty, and fidelity tendencies.",
    "hero": "Assess your loyalty in relationships.",
    "faq": [
        {"q": "What does the Loyalty Test measure?", "a": "It scores your loyalty level across commitment, honesty, and fidelity tendencies."},
        {"q": "What does a low loyalty score mean?", "a": "It may indicate weaker commitment signals — useful to reflect on before serious relationships."},
        {"q": "Is this a scientific test?", "a": "No — it's a self-assessment for reflection, not a clinical measure."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"male-delusion-calculator": {
    "title": "Male Delusion Calculator – Dating Standards Reality Check",
    "meta": "Test whether your dating filters are realistic with the viral Male Delusion Calculator. Free, no sign-up.",
    "hero": "Test whether your dating standards match demographic reality.",
    "faq": [
        {"q": "What is the Male Delusion Calculator?", "a": "It's a viral tool that tests whether your dating filters (age, height, income) match the actual available population of women."},
        {"q": "How does it work?", "a": "You set preferences, and the tool applies demographic rates to show the percentage of women who meet them."},
        {"q": "Why are my results so low?", "a": "Strict filters compound — each requirement multiplies against the last and shrinks the pool quickly."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"marriage-compatibility-score": {
    "title": "Marriage Compatibility Score – Are You Marriage-Ready Together?",
    "meta": "Score marriage compatibility between partners. Free tool rating values, finances, family goals, and conflict style.",
    "hero": "Score long-term marriage compatibility between two partners.",
    "faq": [
        {"q": "What does the Marriage Compatibility Score measure?", "a": "It scores marriage-readiness alignment across values, finances, family goals, and conflict style."},
        {"q": "What predicts marriage success?", "a": "Shared values, aligned family goals, and healthy conflict resolution are consistently cited predictors."},
        {"q": "Is this a predictor of divorce?", "a": "No — it's a directional self-assessment, not a statistical predictor."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"name-compatibility-calculator": {
    "title": "Name Compatibility Calculator – Fun Couples Match",
    "meta": "A fun name compatibility test for couples. Free tool that scores name letters and numerological patterns for entertainment.",
    "hero": "A playful name-based compatibility match for couples.",
    "faq": [
        {"q": "What does the Name Compatibility Calculator do?", "a": "It produces a fun compatibility score from the letters and patterns in two names — for entertainment."},
        {"q": "How is name compatibility calculated?", "a": "The tool maps name letters to values and returns a percentage-style match score."},
        {"q": "Is name compatibility real?", "a": "No — it's purely for fun. There is no scientific basis for name-based compatibility."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"partner-availability-calculator": {
    "title": "Partner Availability Calculator – How Likely Is a Match?",
    "meta": "Estimate how available a partner is for a relationship. Free tool scoring emotional readiness and life circumstances.",
    "hero": "Estimate how available a potential partner is.",
    "faq": [
        {"q": "What does the Partner Availability Calculator measure?", "a": "It estimates how available a partner is for a relationship, based on emotional readiness and life circumstances."},
        {"q": "What signals low availability?", "a": "Unclear commitment, busy life circumstances, and unresolved past relationships all lower availability."},
        {"q": "Who should use this tool?", "a": "Anyone evaluating whether a match is realistically available for a relationship."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"partner-effort-calculator": {
    "title": "Partner Effort Calculator – Is the Effort Equal?",
    "meta": "Assess whether relationship effort is balanced. Free tool scoring initiative, responsiveness, and investment on both sides.",
    "hero": "Assess whether relationship effort is balanced between partners.",
    "faq": [
        {"q": "What does the Partner Effort Calculator measure?", "a": "It scores the balance of effort between partners — initiative, responsiveness, and investment."},
        {"q": "Why does effort balance matter?", "a": "One-sided effort is a common source of resentment and relationship strain."},
        {"q": "How is the score calculated?", "a": "You rate each partner's effort behaviors, and the tool compares them into a balance score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"partner-income-calculator": {
    "title": "Partner Income Calculator – Does Income Matter to You?",
    "meta": "See how partner income expectations affect your dating pool. Free tool comparing income filters to demographic reality.",
    "hero": "See how income expectations shrink or expand your dating pool.",
    "faq": [
        {"q": "What does the Partner Income Calculator do?", "a": "It shows how your partner income requirements affect the size of your realistic dating pool."},
        {"q": "How does income affect the pool?", "a": "Higher income thresholds exclude a larger share of the population, shrinking the matching percentage."},
        {"q": "Should income be a filter?", "a": "That's personal — the tool only shows the demographic impact of the filter, not whether to use it."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"partner-loyalty-score": {
    "title": "Partner Loyalty Score – How Loyal Is Your Partner?",
    "meta": "Estimate a partner's loyalty from relationship signals. Free tool scoring honesty, consistency, and commitment.",
    "hero": "Estimate a partner's loyalty from observable signals.",
    "faq": [
        {"q": "What does the Partner Loyalty Score estimate?", "a": "It estimates a partner's loyalty from honesty, consistency, and commitment signals you observe."},
        {"q": "What signals indicate high loyalty?", "a": "Consistent behavior, honesty, and clear commitment generally indicate higher loyalty."},
        {"q": "Is this a reliable assessment?", "a": "No — it's a directional estimate based on your observations, not a definitive judgment."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"partner-realism-calculator": {
    "title": "Partner Realism Calculator – Is Your Partner Type Realistic?",
    "meta": "Check whether your ideal partner criteria are realistic. Free tool comparing your preferences to demographic data.",
    "hero": "Check whether your ideal-partner criteria are realistic.",
    "faq": [
        {"q": "What does the Partner Realism Calculator do?", "a": "It compares your ideal partner criteria against demographic data to show how realistic they are."},
        {"q": "How do I know if my type is realistic?", "a": "If your combined criteria match only a tiny percentage of the population, your type may be unrealistic."},
        {"q": "Should I change my standards?", "a": "That's your call — the tool only quantifies how rare your criteria combination is."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"personality-compatibility-calculator": {
    "title": "Personality Compatibility Calculator – Do Personalities Fit?",
    "meta": "Score personality compatibility between partners. Free tool rating temperament, communication style, and values.",
    "hero": "Score how well two personalities fit together.",
    "faq": [
        {"q": "What does the Personality Compatibility Calculator measure?", "a": "It scores personality alignment between partners across temperament, communication style, and values."},
        {"q": "Do opposites really attract?", "a": "Sometimes, but research suggests shared values matter more than complementary differences for long-term satisfaction."},
        {"q": "How is the score calculated?", "a": "You rate personality traits for both partners, and the tool returns a 0–100% alignment score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"personality-match-calculator": {
    "title": "Personality Match Calculator – Free Compatibility Score",
    "meta": "Calculate personality match between two people. Free tool scoring trait alignment into a 0–100% compatibility estimate.",
    "hero": "Calculate a personality match score between two people.",
    "faq": [
        {"q": "What does the Personality Match Calculator do?", "a": "It calculates a compatibility score from the personality-trait alignment between two people."},
        {"q": "How is personality match scored?", "a": "You rate traits for both people, and the tool computes an alignment percentage."},
        {"q": "Who is this for?", "a": "Couples or friends curious about how their personalities align."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"relationship-drama-score": {
    "title": "Relationship Drama Score – How Much Drama Is There?",
    "meta": "Measure the level of drama in a relationship. Free tool scoring conflict frequency, jealousy, and emotional intensity.",
    "hero": "Measure how much drama exists in a relationship.",
    "faq": [
        {"q": "What does the Relationship Drama Score measure?", "a": "It scores the level of drama in a relationship — conflict frequency, jealousy, and emotional intensity."},
        {"q": "What causes high relationship drama?", "a": "Frequent conflict, jealousy, and emotional volatility typically raise the drama score."},
        {"q": "Is some drama normal?", "a": "Occasional conflict is normal; the tool helps you see whether yours is elevated."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"relationship-investment-calculator": {
    "title": "Relationship Investment Calculator – Who's Investing More?",
    "meta": "Compare relationship investment between partners. Free tool scoring time, energy, and emotional investment balance.",
    "hero": "Compare how much each partner is investing in the relationship.",
    "faq": [
        {"q": "What does the Relationship Investment Calculator measure?", "a": "It compares the time, energy, and emotional investment each partner puts into the relationship."},
        {"q": "Why does investment balance matter?", "a": "Uneven investment often signals imbalance and predicts future dissatisfaction."},
        {"q": "How is investment scored?", "a": "You rate each partner's investment behaviors, and the tool returns a balance comparison."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"relationship-red-flag-test": {
    "title": "Relationship Red Flag Test – Spot the Warning Signs",
    "meta": "Identify red flags in a relationship with a free self-assessment. Score control, disrespect, and dishonesty signals.",
    "hero": "Identify red flags in your relationship.",
    "faq": [
        {"q": "What does the Red Flag Test do?", "a": "It scores the presence of warning signs — control, disrespect, dishonesty — in a relationship."},
        {"q": "What are common red flags?", "a": "Controlling behavior, disrespect, dishonesty, and isolation from friends or family are common ones."},
        {"q": "What if I score high on red flags?", "a": "A high score suggests patterns worth taking seriously — consider discussing them or seeking support."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"relationship-stability-calculator": {
    "title": "Relationship Stability Calculator – How Stable Are You Two?",
    "meta": "Estimate relationship stability from conflict, commitment, and compatibility factors. Free 0–100% stability score.",
    "hero": "Estimate how stable a relationship is likely to be.",
    "faq": [
        {"q": "What does the Relationship Stability Calculator measure?", "a": "It estimates stability from conflict patterns, commitment, and compatibility factors."},
        {"q": "What makes a relationship stable?", "a": "Low destructive conflict, strong commitment, and core compatibility are the main contributors."},
        {"q": "Is stability the same as happiness?", "a": "Not exactly — a stable relationship isn't always happy, and vice versa. The tool focuses on stability."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"relationship-toxicity-test": {
    "title": "Relationship Toxicity Test – Is It Toxic?",
    "meta": "Assess relationship toxicity with a free self-test. Score manipulation, criticism, and control patterns.",
    "hero": "Assess whether a relationship has toxic patterns.",
    "faq": [
        {"q": "What does the Toxicity Test measure?", "a": "It scores toxic patterns — manipulation, criticism, and control — in a relationship."},
        {"q": "What are signs of a toxic relationship?", "a": "Constant criticism, manipulation, and feeling drained or controlled are common signs."},
        {"q": "What should I do with a high score?", "a": "A high score suggests unhealthy patterns — consider professional support or evaluating the relationship."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"situationship-probability-test": {
    "title": "Situationship Probability Test – Is It Going Nowhere?",
    "meta": "Estimate whether a connection is stuck in a situationship. Free tool scoring commitment and clarity signals.",
    "hero": "Estimate whether a connection is likely to stay a situationship.",
    "faq": [
        {"q": "What does the Situationship Probability Test do?", "a": "It estimates whether a connection is likely to remain undefined (a situationship) based on commitment and clarity signals."},
        {"q": "What signals a situationship?", "a": "Vague labels, inconsistent communication, and no forward momentum are classic signs."},
        {"q": "How do I get out of a situationship?", "a": "The tool doesn't advise, but clarity about what you want is the usual first step."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"soulmate-probability": {
    "title": "Soulmate Probability – What Are the Odds?",
    "meta": "Estimate the probability of finding your soulmate. Free tool combining pool size, compatibility, and timing factors.",
    "hero": "Estimate the probability of finding your soulmate.",
    "faq": [
        {"q": "What does the Soulmate Probability tool estimate?", "a": "It estimates the probability of finding a soulmate, combining pool size, compatibility, and timing factors."},
        {"q": "Is there really a 'soulmate'?", "a": "That's a personal belief — the tool treats it as a fun probability exercise, not a claim about destiny."},
        {"q": "Why is the probability so low?", "a": "Combining strict compatibility with pool size and timing compounds into a small percentage."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"texting-compatibility-calculator": {
    "title": "Texting Compatibility Calculator – Do Your Texting Styles Match?",
    "meta": "Score texting compatibility between partners. Free tool rating response style, frequency, and tone alignment.",
    "hero": "Score how well two texting styles align.",
    "faq": [
        {"q": "What does the Texting Compatibility Calculator measure?", "a": "It scores alignment on texting style — response time, frequency, and tone — between partners."},
        {"q": "Why does texting compatibility matter?", "a": "Texting is a primary communication channel in modern dating, and style mismatches cause friction."},
        {"q": "How is the score calculated?", "a": "You rate each person's texting habits, and the tool returns an alignment score."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"trust-score-test": {
    "title": "Trust Score Test – How Trusting Are You?",
    "meta": "Assess your trust level in relationships with a free self-test. Score openness, past hurt, and suspicion tendencies.",
    "hero": "Assess your trust level in relationships.",
    "faq": [
        {"q": "What does the Trust Score Test measure?", "a": "It scores your trust level across openness, past hurt, and suspicion tendencies."},
        {"q": "What does a low trust score mean?", "a": "It may indicate difficulty trusting others, often from past experiences — worth reflecting on."},
        {"q": "Is this a clinical test?", "a": "No — it's a self-reflection tool, not a psychological assessment."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
"zodiac-compatibility-calculator": {
    "title": "Zodiac Compatibility Calculator – Fun Astrology Match",
    "meta": "Check zodiac sign compatibility with a free astrology match tool. Fun entertainment score for couples.",
    "hero": "A fun zodiac-based compatibility match for couples.",
    "faq": [
        {"q": "What does the Zodiac Compatibility Calculator do?", "a": "It produces a fun compatibility score from zodiac sign pairings — for entertainment."},
        {"q": "How is zodiac compatibility calculated?", "a": "The tool maps sign pairings to a traditional compatibility matrix and returns a percentage-style score."},
        {"q": "Is zodiac compatibility real?", "a": "No — astrology is not scientifically validated. Treat the result as entertainment only."},
        SHARED_ACCURACY, SHARED_FREE,
    ],
},
}

def apply(slug, c, base="tools"):
    path = os.path.join(base, slug, "index.html")
    if not os.path.exists(path):
        print(f"SKIP (missing) {slug}")
        return
    with open(path, encoding="utf-8") as f:
        h = f.read()
    # title
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(c['title'])}</title>", h, count=1)
    # meta description
    h = re.sub(r'<meta name="description" content=".*?"\s*/?>', f'<meta name="description" content="{html.escape(c["meta"], quote=True)}" />', h, count=1)
    # hero description
    h = re.sub(r'<p class="hero-description">.*?</p>', f'<p class="hero-description">{html.escape(c["hero"])}</p>', h, count=1)
    # FAQPage JSON-LD
    faq_entries = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (html.escape(x["q"], quote=True), html.escape(x["a"], quote=True))
        for x in c["faq"]
    )
    new_faq = '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + faq_entries + "]}"
    h, n = re.subn(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>',
                   '<script type="application/ld+json">' + new_faq + "</script>", h, count=1, flags=re.S)
    # also update WebApplication description to match meta
    h = re.sub(r'("description":")([^"]*)(","offers")', lambda m: m.group(1) + html.escape(c["meta"], quote=True) + m.group(3), h, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK {slug} (faq replaced: {n})")

if __name__ == "__main__":
    for slug in TOOLS:
        apply(slug, TOOLS[slug])
    print(f"\nDone. {len(TOOLS)} tools processed.")

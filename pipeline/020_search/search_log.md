# Novelty search log

Totals: 226 web searches, 19 full-text reads.
Date: 2026-11-23. LLM-assisted search (Claude Sonnet subagents with WebSearch and WebFetch), verified by full-text reads. Extracted from the run logs; queries are verbatim.

Extra checks by hand in a browser: Google Scholar "cited by" for [1] (no citing papers); OpenReview forum of [1] (no public reviews).

Known gaps: pre-2023 work; control theory, operations research and economics vocabularies; non-English surveys; Semantic Scholar citation lists (HTTP 429).

## Round 1: replies to [1], transfer critiques, agenda papers, per-problem prior work

- Web searches: 57. Page fetches by site: arxiv.org 38, icml.cc 5, api.semanticscholar.org 2, raillab.org 2, scholar.google.com 2, neurips.cc 2, lesswrong.com 2, openreview.net 1, mdpi-res.com 1.
- Full-text reads: 5 of 5 attempted: AI Agent Safety is a Reinforcement Learning Problem (McLean et al., AIWILD @ ICML 2026); Safe In-Context Reinforcement Learning (SCARED), ICML 2026; Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols; Mitigating Agentic Deception via Evaluation-Side Partially Observable Games (e-PoG); From Refusal to Recovery: A Control-Theoretic Approach to Generative AI Guardrails.

Queries:

1. prompt injection as reward corruption reinforcement learning authenticated instructions LLM agents
2. assistance games CIRL large language models natural language reward preference manipulation
3. impact measures side effects attainable utility LLM tool-using agents arXiv
4. safe exploration in-context reinforcement learning safety constraints LLM in-context learners
5. irreversible actions LLM agents one-shot safety guarantee single trial no reset arXiv
6. AI control monitoring game theory auditing deterrence threshold untrusted agent monitor arXiv
7. attributing LLM behavior to pretraining versus RL post-training behavioral attribution
8. "AI Agent Safety is a Reinforcement Learning Problem"
9. reward tampering prompt injection agent "reward hacking" instructions in data channel corrupt objective formal model
10. AI manipulation of user preferences assistance game language model assistant "preference shift" OR "changing preferences" RL framework
11. attainable utility preservation language model agents side effects tool use benchmark
12. monitor-aware agents evade monitoring game-theoretic audit policy untrusted LLM agent equilibrium
13. cryptographically authenticated instructions prompt injection defense LLM agent trusted principal signed instructions
14. assistance game endogenous preferences LLM assistant human preference change formal AI alignment arXiv
15. "AI Agent Safety is a Reinforcement Learning Problem"
16. LLM agents as POMDP safe reinforcement learning position paper 2026
17. constrained MDP shielding LLM agent safety does not transfer prompt injection position paper
18. LessWrong OR "Alignment Forum" "agent safety is a reinforcement learning problem"
19. arXiv 2026 safe reinforcement learning tools LLM agents assumptions fail in-context learning frozen weights prompt injection
20. "agent safety" "reinforcement learning" position paper critique safe RL does not apply language model agents 2026 arxiv
21. LessWrong OR "Alignment Forum" "agent safety is a reinforcement learning problem"
22. arXiv 2026 safe reinforcement learning tools LLM agents assumptions fail in-context learning frozen weights prompt injection
23. "agent safety" "reinforcement learning" position paper critique safe RL does not apply language model agents 2026 arxiv
24. arXiv 2026 "Language agents" POMDP formalization safety "belief state" LLM agent position
25. arXiv 2026 safe exploration in-context learning LLM agents constrained MDP no training-time control
26. arXiv 2026 "Language agents" POMDP formalization safety "belief state" LLM agent position
27. arXiv 2026 safe exploration in-context learning LLM agents constrained MDP no training-time control
28. McLean 2026 "AI Agent Safety is a Reinforcement Learning Problem" cited by
29. LLM agent safety monitoring as a game agent models its monitor, endogenous reward human preference manipulation assistance game 2026 arXiv
30. McLean 2026 "AI Agent Safety is a Reinforcement Learning Problem" cited by
31. LLM agent safety monitoring as a game agent models its monitor, endogenous reward human preference manipulation assistance game 2026 arXiv
32. Foundational Challenges in Assuring Alignment and Safety of Large Language Models arXiv
33. Alignment of Language Agents Kenton 2021 arXiv
34. Unsolved Problems in ML Safety Hendrycks arXiv
35. agentic AI safety open problems research agenda 2025 arXiv
36. safe reinforcement learning for LLM agents survey open problems prompt injection constrained MDP shielding
37. "AI Agent Safety is a Reinforcement Learning Problem"
38. International AI Safety Report 2026 agents open challenges
39. Open Problems in Technical AI Governance arXiv
40. safe exploration in-context learning LLM agents no weight updates open problem safe RL assumptions do not hold
41. LLM agents are not MDPs: assumptions of reinforcement learning safety fail prompt injection endogenous preferences position paper
42. reinforcement learning safety lens for LLM agents critique transfer of safe RL methods to language agents preconditions
43. openreview McLean "AI Agent Safety is a Reinforcement Learning Problem" AIWILD response OR rebuttal OR critique
44. assistance games LLM agents preference manipulation endogenous preferences open problem language models
45. authenticated objectives instruction hierarchy LLM agents open problem prompt injection data-instruction separation fundamental
46. "AI Agent Safety is a Reinforcement Learning Problem"
47. position paper safe reinforcement learning assumptions do not hold for LLM agents constrained MDP shielding
48. survey safe reinforcement learning meets large language models safety constrained MDP LLM
49. shielding LLM agents runtime enforcement assumptions known safety specification critique arxiv
50. arxiv "is not a reinforcement learning problem" LLM agents position paper safety
51. safe exploration in-context learning LLM agents frozen weights safe RL does not apply
52. prompt injection agent POMDP objective not fixed safe RL assumption reward specification endogenous preferences LLM agents
53. position: agent safety constrained Markov decision process LLM agents limitations cost function unknown tool use
54. "does not imply" method transfer formal equivalence LLM agents reinforcement learning framing critique position paper
55. position paper "safe RL" assumptions LLM agents deployment single trial no resets monitoring game agent models its monitor
56. LessWrong Alignment Forum safe RL techniques constrained optimization shielding do not transfer to LLM agents assumptions
57. agentic AI safety "reinforcement learning" lessons assumptions mismatch LLM agents reward hacking safe RL transfer position 2026

## Round 2: five claims (A–E) x two methods (keyword, citation chasing)

- Web searches: 166. Page fetches by site: arxiv.org 61, icml.cc 7, raillab.org 2, api.semanticscholar.org 2, iclr-blogposts.github.io 1, neurips.cc 1, github.com 1, semanticscholar.org 1, theorempath.com 1, lacuna.tiptreesystems.com 1.
- Full-text reads: 7 of 8 attempted: RL in Name Only? Analyzing the Structural Assumptions in RL post-training for LLMs; Reinforcement Learning from Human Feedback (Lambert RLHF book), v7 Section 3.1.3 (text read is v12, 11 Sep 2026); RLHF without RL - Direct Preference Optimization (ICLR 2024 blog track); Invariance in Policy Optimisation and Partial Identifiability in Reward Learning; Reinforcement Learning from Human Feedback: A Statistical Perspective; On the Limits of Reinforcement Learning for LLM-Agent Safety: Formal Equivalence Is Not Method Transfer (repo: Rebuttal to 'AI Agent Safety is an RL Problem'); AI Agent Safety is a Reinforcement Learning Problem (McLean et al., ICML 2026 AIWILD).

Queries:

1. "AI Agent Safety is a Reinforcement Learning Problem" McLean
2. RLHF LLM contextual bandit single-step MDP versus agentic RL multi-turn POMDP taxonomy of settings
3. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey degenerate single-step MDP vs POMDP
4. safe reinforcement learning LLM agents irreversible actions observation ambiguity reward misspecification position paper
5. cites "AI Agent Safety is a Reinforcement Learning Problem" safe RL LLM agents shielding CMDP assumptions
6. process reward model token-level MDP deterministic tree RLHF bandit RLVR GRPO "contextual bandit" formalization LLM reinforcement learning is not RL
7. LLM agents safety "no reset" irreversible long-horizon autonomous agent versus chatbot RLHF different decision problem safe RL does not transfer
8. Rethinking Agentic Reinforcement Learning In Large Language Models arXiv 2604.27859 degenerate MDP POMDP formulations
9. reward model overoptimization RLHF vs tool agent irreversible actions vs partial observability: where do safe RL assumptions break for LLMs
10. LLM agent as POMDP formal framework safety tool-use ambiguity observation "agent safety" reinforcement learning perspective survey 2026
11. "McLean" 2026 agent safety reinforcement learning problem response commentary OR rebuttal OR "builds on" safe RL assumptions LLM agents
12. LessWrong Alignment Forum LLM RL settings differ RLHF bandit RLVR agents POMDP "not the same" reinforcement learning concepts mapping
13. "AI agent safety" "reinforcement learning problem" 2026 cited OR responds OR "McLean et al." agents in the wild safe exploration reward misspecification partial observability LLM
14. "AI agent safety" "reinforcement learning problem" 2026 cited OR responds OR "McLean et al." agents in the wild safe exploration reward misspecification partial observability LLM
15. RLHF is a contextual bandit, not a full MDP; LLM post-training decision problem formulation bandit vs MDP vs POMDP
16. "The Landscape of Agentic Reinforcement Learning for LLMs" survey degenerate single-step MDP vs POMDP
17. "RL in Name Only" structural assumptions RL post-training LLMs deterministic transitions
18. taxonomy of LLM RL settings: RLHF bandit, process reward MDP, tool-using agent POMDP, which reinforcement learning concepts apply
19. "AI Agent Safety is a Reinforcement Learning Problem" McLean
20. LLM agents RL assumptions break: no reset, partial observability, adversarial environment, safe RL guarantees do not transfer to LLM agents
21. Lambert RLHF book "contextual bandit" "not a full MDP" bandit formulation language model rewards whole response
22. RLVR "contextual bandit" GRPO verifiable rewards is not reinforcement learning no credit assignment trajectory
23. process reward model step-level MDP deterministic tree LLM reasoning formalization outcome reward bandit
24. what is reinforcement learning in LLM alignment? mismatch between classical RL assumptions and RLHF position paper
25. autonomous LLM agents long-horizon POMDP no episode reset deployment safety classical RL assumptions fail
26. LessWrong RLHF is not really reinforcement learning bandit single step episode language models
27. "Foundational Challenges in Assuring Alignment and Safety of Large Language Models" RL formulation bandit agents POMDP
28. reinforcement learning for LLMs tutorial MDP formulation bandit vs token-level vs multi-turn agent which RL concepts transfer table comparison
29. process reward model step-level MDP RL for LLM closest to classical RL; DeepSeek-R1 abandoned PRM reward hacking
30. RLHF LLM contextual bandit not MDP "single-step" token-level MDP agentic RL multi-turn POMDP survey
31. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey degenerate single-step MDP vs POMDP
32. position paper RL vocabulary LLM agents does not transfer reward state "reset" autonomous agents not reinforcement learning
33. "RL in Name Only" structural assumptions RL post-training LLMs deterministic tree MDP process reward
34. DeepSeek-R1 "process reward model" "reward hacking" "retraining the reward model" unsuccessful attempts PRM abandoned
35. taxonomy of LLM reinforcement learning settings RLHF RLVR process reward agentic: which are genuinely sequential decision problems
36. formalization LLM agents as POMDP no reset no reward at deployment safe RL assumptions do not hold LLM agents
37. "AI Agent Safety is a Reinforcement Learning Problem" McLean
38. LLM RL "bandit" "process reward" "agentic" spectrum from bandit to full MDP; how much RL is in RL for LLMs blog
39. Lambert RLHF book "bandit" problem formulation "not a full MDP" language models reward model process reward models fell out of favor
40. process reward models fell out of favor frontier labs outcome rewards only reward hacking PRM why abandoned 2025
41. "words transfer" reinforcement learning terminology LLM agents misuse "credit assignment" "exploration" "reward" agents not RL critique 2026
42. Is RLHF really reinforcement learning? bandit vs MDP LLM, RLVR "not really RL", agentic multi-turn "real RL" blog
43. reward identifiability potential shaping Bradley-Terry reward model only within-prompt differences RLHF
44. RLHF is contextual bandit not full MDP; RLVR verifiable reward; agentic RL POMDP survey "from LLM reasoning to autonomous agents"
45. reward model identifiability Bradley-Terry prompt-dependent shift invariance non-identifiable reward RLHF
46. deployed LLM agents have no reward at deployment reward misspecification no object position paper
47. Invariance in Policy Optimisation and Partial Identifiability in Reward Learning
48. RLHF language model as contextual bandit single-step MDP "token-level MDP" versus bandit formulation
49. RLVR verifier reward defined only on checkable domain; reward undefined outside verifiable tasks; agentic RL no reward at deployment
50. formalizing LLM agents reinforcement learning taxonomy chatbot vs agent POMDP what changes reward state reset position paper
51. reward misspecification meaningless after deployment; no reward signal at inference; alignment agents "no reward" at deployment objective not reward-maximizer
52. Agentic RL survey LLM RL "degenerate single-step MDP" versus multi-turn POMDP reward verifiable preference process reward comparison table
53. "AI Agent Safety is a Reinforcement Learning Problem" McLean
54. reward model absolute scale not identifiable across prompts Bradley-Terry only relative; RLHF reward misspecification identifiability position
55. LLM post-training settings differ in reward identifiability: preference, verifiable, process, agentic; what reward means for autonomous agents without episodes
56. LessWrong agents are not reward maximizers at deployment "reward is not the optimization target" LLM no reward at inference
57. RLHF as contextual bandit, process reward step-level MDP, tool-using agent POMDP, taxonomy of LLM RL settings
58. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey degenerate single-step MDP vs POMDP
59. RLHF is a contextual bandit not full MDP LLM alignment formalization position paper
60. "AI Agent Safety is a Reinforcement Learning Problem"
61. token-level MDP vs sentence-level bandit LLM RLHF formulation "From r to Q*" OR "Reinforcement Learning for Language Models" survey
62. LLM agents formalized as POMDP long-horizon no reset safe RL assumptions do not transfer to language model agents
63. RLVR GRPO contextual bandit credit assignment process reward model step-level MDP agentic multi-turn POMDP comparison table concepts
64. position paper "language model" "is not" reinforcement learning agent: which RL concepts apply to RLHF (exploration, state, reset, credit assignment)
65. formalizing LLM agents decision process taxonomy single-turn bandit multi-turn MDP POMDP survey agentic reinforcement learning 2025 2026
66. safe reinforcement learning assumptions fail for LLM agents CMDP shielding autonomous agents position paper 2026
67. RL for LLM reasoning "deterministic tree" MDP process reward model step as action tree search formulation
68. autonomous LLM agent no reset non-episodic deployment adversarial environment no reward at run time reinforcement learning framing mismatch
69. "contextual bandit" RLHF "POMDP" agents "which assumptions" RL theory transfer to LLM post-training critical examination
70. "RL in Name Only" structural assumptions RL post-training LLMs
71. Landscape of Agentic Reinforcement Learning for LLMs survey degenerate single-step MDP versus POMDP
72. RLHF is a contextual bandit not a full MDP LLM token-level MDP step-level process reward
73. DeepSeek-R1 abandoned process reward model reward hacking outcome reward
74. "AI Agent Safety is a Reinforcement Learning Problem" McLean
75. LLM RL taxonomy of settings: RLHF bandit, RLVR, process reward, agentic multi-turn POMDP how far from classical RL
76. "words transfer" RL terminology LLM agents misuse reinforcement learning vocabulary "not RL" position paper
77. is RLVR really reinforcement learning? bandit, no credit assignment, no exploration, no state, position paper LLM
78. process reward model deterministic tree MDP reasoning steps as actions reward hacking PRM
79. Open Problems and Fundamental Limitations of RLHF: RLHF as contextual bandit, reward hacking, "not a true RL"
80. Lambert RLHF book "contextual bandit" "token-level" MDP formulation LLM post-training problem setup
81. Reward hacking in language model agents: revisiting AI Safety Gridworlds
82. LLM reasoning RL spectrum from bandit to MDP: outcome reward vs process reward step-level MDP "closest to" classical reinforcement learning
83. "Decision-Process Cards" Rethinking How RL Claims Are Reported arXiv
84. agentic RL is not really RL: no reset, no reward at deployment, long-horizon autonomous agent versus RLVR formalization gap blog
85. Foundational Challenges in Assuring Alignment and Safety of Large Language Models RL-based finetuning reward model bandit agents
86. Lilian Weng reward hacking in reinforcement learning LLM RLHF process reward
87. safe RL guarantees do not transfer to LLM agents assumptions CMDP shielding LLM agent safety gap
88. process reward models fell out of favor; frontier labs use outcome verifiable rewards instead; PRM is closest to true RL credit assignment but hackable
89. RLHF "not reinforcement learning" contextual bandit LLM alignment blog "no sequential" real RL agents differ interconnects
90. LLM agents safety "reinforcement learning" terminology borrowed: reward, policy, state, exploration, do not mean the same; formal mismatch survey 2026
91. Agent safety should be a runtime contract enforced by the harness arXiv 2608.11274
92. RL in Name Only? Analyzing the Structural Assumptions in RL post-training for LLMs
93. AI Agent Safety is a Reinforcement Learning Problem McLean
94. RLHF contextual bandit versus agentic MDP assumptions differ: state, reset, observations, taxonomy of LLM decision settings
95. safe reinforcement learning assumptions fail for LLM agents prompt injection shielding constrained MDP
96. Agent safety should be a runtime contract
97. Reward hacking in language model agents: revisiting AI Safety Gridworlds
98. Foundational Challenges in Assuring Alignment and Safety of Large Language Models agentic RL assumptions
99. LLM agents violate standard RL assumptions: no reset, partial observability, non-stationary, adversarial observations, no reward at deployment
100. "degenerate MDP" LLM RLHF single-step versus multi-turn agent RL formalization survey
101. why safe RL guarantees do not transfer to LLM agents: Markov state, episodic resets, constrained policy optimization, prompt injection position paper
102. Open Problems and Fundamental Limitations of RLHF contextual bandit not MDP; RLHF versus RL assumptions differ
103. RLVR RLHF "no reset" OR "episodic" LLM agents deployment non-episodic safety gap training vs deployment RL formalism comparison table
104. indirect prompt injection modifies agent objective POMDP adversarial observations formal model reward tampering LLM agent
105. safe reinforcement learning for large language models survey constrained MDP RLHF safe RLHF assumptions limitations
106. formalizing LLM agents as POMDP taxonomy of settings chatbot RLHF bandit, reasoning MDP, tool agent POMDP; what RL theory applies
107. Lil'Log OR Interconnects OR LessWrong RLHF is a contextual bandit not real RL; agents are real RL; implications for safety
108. "AI Agent Safety is a Reinforcement Learning Problem" McLean
109. LLM RLHF as contextual bandit single-step MDP versus agent multi-step POMDP taxonomy of settings
110. "RL in Name Only" structural assumptions RL post-training LLMs degenerate MDP
111. "Agent safety should be a runtime contract"
112. "Reward hacking in language model agents" revisiting AI Safety Gridworlds
113. agent safety safe reinforcement learning CMDP shielding LLM agents irreversible actions partial observability position paper 2026
114. RLVR vs RLHF vs agentic RL different MDP formulations reward model PRM tree MDP bandit survey formalization LLM reinforcement learning
115. agent safety safe reinforcement learning CMDP shielding LLM agents irreversible actions partial observability position paper 2026
116. RLVR vs RLHF vs agentic RL different MDP formulations reward model PRM tree MDP bandit survey formalization LLM reinforcement learning
117. cites "AI Agent Safety is a Reinforcement Learning Problem" McLean Lee Machado Rosman 2026
118. LLM alignment is not RL: reward model overoptimization, agent irreversible actions, partial observability — different problems in different settings
119. Open Problems and Fundamental Limitations of RLHF misspecification partial observability
120. Lambert RLHF book "problem setup" bandit "agentic" reward model verifiable rewards "not a full MDP"
121. "Foundational Challenges in Assuring Alignment and Safety of Large Language Models" agentic LLM irreversible actions reward misspecification
122. autonomous LLM agents safe exploration irreversible actions no reset safe RL gap LLM agents safe RL assumptions violated
123. Semantic Scholar "AI Agent Safety is a Reinforcement Learning Problem" citations
124. "token-level MDP" "contextual bandit" process reward model "tree" LLM reasoning formulation agent multi-turn POMDP comparison settings
125. shielding LLM agents reversibility safe reinforcement learning tool-use agents observation ambiguity prompt injection POMDP
126. LLM agents "safe exploration" survey agentic RL safety risks reward hacking irreversible actions partial observability taxonomy "agentic reinforcement learning" safety
127. "LLM as policy" reinforcement learning formalization chat vs agent horizon reset exploration adversary "no reset" autonomous agents differences from classical RL
128. Lil'Log OR Interconnects OR Gradient "RLHF is a bandit" "agents are a real MDP" LLM reinforcement learning blog
129. LLM agents "safe exploration" survey agentic RL safety risks reward hacking irreversible actions partial observability taxonomy "agentic reinforcement learning" safety
130. "LLM as policy" reinforcement learning formalization chat vs agent horizon reset exploration adversary "no reset" autonomous agents differences from classical RL
131. Lil'Log OR Interconnects OR Gradient "RLHF is a bandit" "agents are a real MDP" LLM reinforcement learning blog
132. response to McLean et al. agent safety RL problem "formal equivalence" not method transfer safe RL guarantees LLM agents assumptions
133. process reward model misspecification verifier reward hacking RLVR false positives reward misspecification in LLM reasoning versus agents irreversible tool actions
134. AI Agent Safety is a Reinforcement Learning Problem McLean
135. RLHF as contextual bandit versus LLM agents multi-turn MDP assumptions differ safe RL taxonomy
136. The Landscape of Agentic Reinforcement Learning for LLMs: A Survey degenerate single-step MDP vs POMDP
137. safe reinforcement learning assumptions do not hold for LLM agents prompt injection shielding constrained MDP position paper
138. formalizing LLM agents as POMDP no reset non-stationary adversarial observations RL theory mismatch
139. Reinforcement learning for LLMs is not really RL: bandit, token-level MDP, credit assignment, position paper
140. "Safety Does Not Compose" Non-Decaying Loop State autonomous LLM agents
141. Agentic Safety is an Epistemic Property, Not a Behavioral One
142. LLM agents violate assumptions of safe reinforcement learning: no resets, learner not under designer control, observations adversarial
143. table comparing RLHF, RLVR, process reward, agentic RL settings state action reward episode definition taxonomy LLM MDP formulations
144. position paper alignment RLHF reward hacking does not transfer to agents deployment no episodes continual autonomy "safe RL" assumptions LLM
145. LLM agent as POMDP prompt injection observation changes the objective reward tampering formal framework
146. LLM safety guarantees from reinforcement learning do not apply: stated assumptions of constrained RL versus language model agents survey of assumption violations
147. "agentic RL" versus "RLHF" differences: environment resets, partial observability, stochastic tool feedback, untrusted observations, comparison table
148. LessWrong Alignment Forum LLM agents are not RL agents: why classical RL safety results (shielding, CPO, safe exploration) do not apply
149. RLVR RLHF agentic settings "policy is not under designer control" OR "no reset" OR "non-episodic" LLM agents continual deployment RL assumptions mismatch
150. A Tutorial on Reinforcement Learning for LLMs RLHF and Beyond contextual bandit MDP POMDP agents
151. Lil'Log OR Interconnects OR Gradient LLM RL is a bandit not a sequential decision problem; agents are the real RL
152. reward identifiability potential shaping Bradley-Terry only within-prompt differences RLHF reward model
153. RLHF reward model Bradley-Terry identifiability up to prompt-dependent shift
154. "RL in Name Only" structural assumptions RL post-training LLMs
155. Landscape of Agentic Reinforcement Learning for LLMs survey degenerate single-step MDP
156. AI Agent Safety is a Reinforcement Learning Problem McLean 2026
157. reward misspecification deployed agents no reward at deployment runtime no reward signal LLM agents
158. RLVR verifiable rewards reward only defined on verifiable domain unverifiable tasks no reward signal limitation
159. reward model contextual bandit prompt-level reward unidentifiable across prompts calibration comparisons only within prompt
160. Open Problems and Fundamental Limitations of RLHF reward misspecification "ill-posed" reward function identifiability
161. LLM RLHF token-level MDP bandit "reward shaping" equivalence potential function DPO implicit reward identifiable only up to function of prompt
162. taxonomy of RL settings for language models: bandit, MDP, POMDP, agentic, what changes reward credit assignment exploration formalization
163. deployed LLM agent no reward signal at deployment objective not specified at runtime alignment cannot be reward optimization argument
164. Lambert RLHF book reward models Bradley-Terry "only" relative preference scale not comparable across prompts
165. autonomous LLM agent deployment no reset no reward signal partially observable adversarial safe RL assumptions do not hold
166. verifier coverage reward hacking RLVR reward undefined outside verified set programmatic verifier incomplete specification

## Round 3: full-text reads of nine priority candidates

- Web searches: 3. Page fetches by site: neurips.cc 1.
- Full-text reads: 7 of 9 attempted: Rethinking Agentic Reinforcement Learning In Large Language Models; Reinforcement Learning in the Era of LLMs: What is Essential? What is needed? An RL Perspective on RLHF, Prompting, and Beyond (Sun, 2023); DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (arXiv 2501.12948v2, Jan 2026 Nature-style revision); Towards Understanding Specification Gaming in Reasoning Models; From Reasoning to Agentic: Credit Assignment in Reinforcement Learning for Large Language Models (Zhang, arXiv 2604.09459 v3); When Your AIs Deceive You: Challenges of Partial Observability in RLHF (Lang et al., NeurIPS 2024); Lambert, Reinforcement Learning from Human Feedback (book), arXiv 2504.12501.

Queries:

1. "Stop Calling It Reinforcement Learning in Language Models Without Clear Improvement Claims" Decision-Process Cards
2. Decision-Process Cards: Rethinking How RL Claims Are Reported Kohli Khandelwal Agarwal Maity Sheth arxiv
3. "Decision-Process Card" LLM RL claims Kohli Sheth pdf openreview OR arxiv OR github


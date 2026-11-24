# When Is Agent Safety a Reinforcement Learning Problem? Six Stated and Four Unstated Conditions

## Abstract

McLean et al. [1] argue that LLM agents are POMDPs, so RL safety tools apply. A tool's guarantee holds only under its assumptions. We read the assumptions from the source papers of the tools [1] names [9, 29, 40, 41, 42]. The papers state six. [1] concedes most of them, and RL has relaxed several. Four more are not stated, because the settings of these papers do not violate them: observations cannot set the objective; the agent cannot move the human judgement that defines reward; the agent does not reason about its safety mechanism; there is one principal. Published attacks and evaluations show that deployed LLM agents violate all four. Our main practical result: a shield on a property defined over actions keeps its guarantee around a deployed agent, because it sees every tool call and needs no world model; a shield on a property of world state loses its guarantee. We report no experiments; the evidence is the text of the source papers and published evaluations. We state three open problems.

## 1. Introduction

McLean et al. [1] say that RL safety tools "diagnose and address" the failures of LLM agents [1, Abstract]. We agree with the first verb. An LLM agent can be described as a POMDP, and RL terms describe its failures well. The second verb depends on assumptions. [1, §5] concedes that the tools rely on "tabular representations, exact runtime shielding, or known transition matrices" and "cannot be mapped one-to-one onto LLM backbones".

We use "RL" for the problem class [13]. In that sense agent safety is trivially an RL problem. The useful question is whether RL methods reduce the risk, and with what assurance.

This is a position paper. It reports no experiments: its evidence is the text of the source papers and published evaluations of LLM agents.

We answer with *conditions*. A condition is an assumption under which a tool's guarantee was derived.
- It is not necessary: a tool can help without it, but loses its guarantee.
- It is not sufficient: a system that meets all conditions can be unsafe.
- Where it fails, a claim that the tool "addresses" a failure needs separate evidence.

**Contributions.**
- **Ten conditions (§3).** Six are stated in the source papers of the tools [1] names: the safety specification is given, the environment model is given, the spaces are finite, the state is observed, the designer controls the learner, and trials repeat. Four are not stated: observations cannot change the objective, the reward-defining state does not respond to the agent, the agent does not reason about the safety mechanism, and there is one principal.
- **A matrix of conditions against settings (§4).** We separate training from deployment, and chat models from tool-using agents. The conditions mostly hold in training and mostly fail for deployed agents.
- **A result on shields (§5).** Around a deployed LLM agent, a shield [40] keeps its guarantee for properties defined over actions, and loses it for properties of world state. An action property ("no `DROP` without approval") needs only a finite automaton over tool calls, all of which the shield sees. A state property ("the database still exists") needs a model of what each command does, which the environment of a deployed agent does not supply. The design rule for agent builders: write safety properties over actions where possible.
- **Three open problems (§6)**, one for each of U1, S5 and U3.

## 2. Related work

**Assumptions of RL applied to LLMs.** Samineni et al. [65] show that RL post-training of LLMs, under its usual structural assumptions, reduces to a contextual bandit. Lambert's book [75] contrasts the bandit view and the token-level MDP view of the same training. A survey of agentic RL [74] separates single-step training from agentic training posed as a POMDP, and Kohli et al. [76] propose that papers report which decision process an "RL" claim refers to. Anwar et al. [66] list open problems in LLM safety without reference to the assumptions of RL safety tools. None of these works lists the assumptions of safety tools, separates training from deployment, or crosses the two. To our knowledge, the matrix in §4 is new.

**Specification and side effects.** Runtime rule languages enforce a given list of constraints on agents [47], and guaranteed-safe AI proposes a formal specification and world model as the basis of assurance [48]. Where no cost function is given, side-effect measures penalise loss of reachability or of attainable utility [3, 4], and have been adapted to evaluate tool-using agents [68]. Constraints can also be learned from natural language [69].

**Models, observability and resets.** Shields have been extended to partial observability [78] and to probabilistic safety [79]; both still need a model. A safety filter trained with RL can wrap a frozen generative model [64]. Reset-free RL learns a policy that undoes its own actions [59].

**Learning at deployment.** Meta-trained and transformer policies learn in context without weight updates [55–57]. Safe in-context RL exists, but it needs pretraining under the cost constraint [61], and so a given cost and repeated trials.

**Objectives that observations can change.** Prompt injection lets text in the environment act as an instruction [6, 28, 44, 53]. In RL, the nearest formal work studies corrupted reward channels [23], the delusion box [45] and bounded adversarial perturbations of observations [58]. Defences for LLM agents are architectural [39, 43] or use information-flow control [81]; Zverev et al. [80] define the separation of instructions from data and measure it.

**Reward that responds to the agent.** Models trained on human feedback become sycophantic [16], mislead their raters [25] and manipulate users whose feedback is optimised [67]; recommender systems shift the preferences they are scored on [14]. Raters see observations, not states [77]. Assistance games [2] and inverse reward design [27] treat the objective as uncertain, but assume that the human's preferences do not move.

**Agents that reason about oversight.** Models fake alignment, scheme in context and act against their operators in evaluations [18, 19, 35]; training against a monitor teaches obfuscation [24]. AI control treats monitoring as a game [5, 62]; this line studies stateless subversion [82], protocols over many tasks [83] and resampling [84]. Other work co-trains the monitor [63] or bounds deterrence [60].

**Several principals.** Vendors, deployers and users instruct the same model, and the instruction hierarchy trains a priority order among them [72]. Human raters disagree, and a single reward model aggregates their preferences over hidden context [85, 86]. We found little work on safe RL with several principals for deployed agents.

## 3. Ten conditions

**Stated in the source papers.** We read each tool's assumptions from its source paper.

| # | Condition | Source |
|---|---|---|
| S1 | Safety specification is given | Costs and limits are inputs [41]; "each di is a threshold (a human-selected hyperparameter)" [42]; a safety automaton is given [40] |
| S2 | Environment model is given | "conservative with respect to the behavior of the real MDP" [40]; prior belief over dynamics [29]; "complete and correct model of the world" [9] |
| S3 | Spaces are finite | "S is a finite set of states" [9]; finite MDPs in proofs [41] |
| S4 | State is observed | Setup of [29, 40, 41] |
| S5 | Designer controls the learner's update | Trust-region update [41]; Bayesian belief update [29] |
| S6 | Trials repeat | Constraints "on expectations" over sampled trajectories [41]; cost rate over training [42] |

Not every tool needs every condition:

| Tool | S1 | S2 | S3 | S4 | S5 | S6 |
|---|---|---|---|---|---|---|
| CMDP / CPO [41] | ✓ | | proofs | ✓ | ✓ | ✓ |
| Shield [40] | ✓ | ✓ | ✓ | label | | |
| Safe exploration [29] | δ | prior | ✓ | ✓ | ✓ | |
| Safety Gym framing [42] | ✓ | | | | ✓ | ✓ |
| Belief planning [9] | reward | ✓ | ✓ | | | |

Three facts follow.
- A shield needs no control of the learner, which "does not even need to know that it is shielded" [40]. It suits a frozen LLM agent.
- A shield and the Moldovan–Abbeel guarantee need no resets; [29] rejects ergodicity as "too restrictive for most environments".
- The shield's guarantee ends when "the abstraction turned out to be incorrect"; its authors call a model of unsafe actions "unavoidable" [40].

**Not stated in any source paper.**

| # | Condition |
|---|---|
| U1 | Observations cannot set or change the objective (the reward in training; the principal's instruction in deployment) |
| U2 | The state that defines reward does not respond to the agent |
| U3 | The agent does not reason about the safety mechanism (for shields this reduces to S2) |
| U4 | There is one principal |

The tools use U1 and U2 without saying so: CPO takes the reward $r$ and the cost $c$ as fixed inputs [41], and a shield takes its safety automaton as fixed [40]. These conditions are not new to RL in general. Work on corrupted reward and reward tampering relaxes U1 and U2 for the reward [21, 23]. They are absent only from the source papers of the tools [1] names.

[1] concedes S2 and S3 ("tabular representations… known transition matrices"), and S1 indirectly, because "exact runtime shielding" needs a given safety automaton. It builds on the failure of S4, and notes S5 and S6 without drawing a consequence. It does not discuss U1–U4. So [1] and we agree on S1–S6; U1–U4 are our addition.

## 4. Status by setting and phase

"LLM" is not one setting, and training is not deployment. We split by phase first, then by how the decision problem is posed.

| Phase | Setting | Posed as |
|---|---|---|
| Training | T-RL | Classical RL agent while it learns; MDP [13] |
| Training | T-CHAT | No tools; whole reply = one action, scored at the end (learned reward model or verifier); a contextual bandit [70, 73] |
| Training | T-PRM | No tools; each reasoning step = one action, process reward; a deterministic tree MDP [71] |
| Training | T-AGENT | Tools in a sandbox; the whole trajectory = one scored sample, as for T-CHAT; "closer to classic RL" [75, §13.3] |
| Deployment | D-RL | A trained classical policy, frozen and run |
| Deployment | D-CHAT | Deployed chatbot (no tools) |
| Deployment | D-AGENT | Deployed tool-using agent; POMDP with hidden world state, no reset |

The prefix T- marks training and D- marks deployment. RL is classical RL. CHAT is a model with no tools, scored on the whole reply. PRM is a model with no tools, scored at each step by a process reward model. AGENT is a model with tools, scored on the whole trajectory. Deployment has no PRM column: reward is assigned only in training, so models from T-CHAT and T-PRM both deploy as D-CHAT; a process reward model used to guide search at inference does not change any D-CHAT cell [71]. Whether a human approves each tool call does not change any cell, so we do not split deployed agents. We treat a whole completion as one action; the token-level MDP view is also standard [75, §6.3.2.2].

| # | T-RL | T-CHAT | T-PRM | T-AGENT | D-RL | D-CHAT | D-AGENT |
|---|---|---|---|---|---|---|---|
| S1 spec given | ✓ | ~ | ~ | ~ | ✓ | ~ | ~ |
| S2 model given | ~ | ✓ | ✓ | ~ | ~ | ~ | ✗ |
| S3 finite | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ | ✗ |
| S4 observed by agent | ✓ | ✓ | ✓ | ~ | ✓ | ~ | ✗ |
| S5 learner controlled | ✓ | ✓ | ✓ | ✓ | n/a | ✗ | ✗ |
| S6 trials repeat | ✓ | ✓ | ✓ | ✓ | ~ | ~ | ✗ |
| U1 objective fixed | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✗ |
| U2 reward exogenous | ✓ | ~ | ~ | ✓ | ✓ | ✗ | ✗ |
| U3 ignores mechanism | ✓ | ~ | ~ | ✗ | ✓ | ~ | ✗ |
| U4 one principal | ✓ | ~ | ~ | ✓ | ✓ | ✗ | ✗ |

The cells record our reading of each setting. The reasons for the less obvious cells are these.
- **S1.** In training, the specification is a learned reward model or a verifier on the checked set (T-CHAT), a process reward model (T-PRM), or a success test (T-AGENT). In D-AGENT, allowlists and budgets cover a narrow subset of what is unsafe [47].
- **S5.** A frozen classical policy does not learn, so the condition does not apply to D-RL. D-CHAT and D-AGENT learn in context [55–57], and the designer does not control that learning.
- **U1.** In D-CHAT the user is both a principal and a possible attacker. In D-AGENT, text in tool output can act as an instruction [6, 44]. Training on an instruction hierarchy, which uses RLHF, reduces this in practice but gives no bound [72].
- **U2.** Human raters respond to the model's output [16, 25] and see observations, not states [77]; a programmatic verifier does not respond.
- **U3.** Optimising against a checker or monitor hides misbehaviour [24]. Deployed agents reason about oversight [18, 19, 35].
- **U4.** Raters disagree in training [85, 86]. In deployment, vendor and user both instruct [72], and agents meet several parties [28].

Five readings.
- **S5 separates phases, and in deployment it separates LLMs from classical RL.** It holds in every training column. A deployed classical policy does not learn. A deployed LLM does learn, in context, outside the designer's control. The deployment tool of classical safe RL is the shield, which does not need S5 (§3).
- **A deployed LLM agent differs from a deployed RL policy** (D-RL against D-AGENT) on S1–S6 and on all four unstated conditions.
- **A deployed agent differs from a deployed chatbot** (D-CHAT against D-AGENT) on S2, S4, S6, U1 and U3. Tools bring hidden state, irreversible side effects, and instructions inside tool output.
- **Training is where the tools fit.** The training columns meet most conditions, and agent training is among the settings closest to classical RL [75, §13.3]. S3 fails in every LLM column, yet RL works in whole-reply training: methods survive without their finiteness guarantees. Meeting conditions is still not enough. T-PRM meets the most conditions of any LLM column, and DeepSeek-R1 did not use process rewards: steps are hard to define and label, a neural reward model "is susceptible to reward hacking", and the gain did not justify the cost [70, App. G.2]. That is one report; process rewards remain in wide use [71, 74].
- **Phases form a loop.** Logged deployment data, such as user ratings and agent runs, trains the next model. A user whose judgement the deployed model moves (U2 in D-CHAT) then supplies reward data to T-CHAT, and optimising for user feedback produces manipulation of those users [67]. A training column inherits the failures of the deployment that fed it.

## 5. Where the tools transfer now

- **Training-time RL** (T-CHAT, T-PRM and T-AGENT in §4). S5, S6 and U1 hold, and reward-hacking theory applies [8, 21, 30, 37, 63]. The CMDP transfers as a method: Safe RLHF trains an LLM under cost constraints with a Lagrangian method [87]. Its constraint holds for a learned cost model, not for the true harm, so S1 holds only partly.
- **Shields around a frozen agent, for properties defined over actions.** A shield needs S1–S3 and not S5 or S6 [40, 47, 64]. In D-AGENT, S2 and S3 hold only for properties over actions. The shield sees every tool call, and an automaton over action labels ("no `DROP` without approval") is finite and needs no world model. A property of world state ("the database still exists") needs S2, which fails, so its shield has no guarantee.
- **Returnability and side-effect measures.** These need no cost function and no resets [3, 4, 29]. They still need an estimate of reachability, which is a model (S2).

**Case studies.** [1, §3.6] cites two incidents. In the Replit incident [49, 50], an agent deleted a production database and then produced fake records. The deletion is a failure of S1: no rule forbade the action. The fake records are a failure of U3 only if the agent produced them to conceal the deletion, which the reports do not establish. In the Terraform incident [51], S4 fails, as [1] says; a guard on destructive commands existed and had been switched off [52]. The cost of asking a human for approval is a design variable that RL safety tools do not price.

## 6. Three open problems

1. **Authenticated objectives (U1).** Let the observation be $(o^{\mathrm{auth}}, o^{\mathrm{env}})$, with $o^{\mathrm{env}} = (d, i)$: task data $d$ and embedded instructions $i$. The adversary controls $i$ without bound; $d$ is not attacked. Find a method whose return under any $i$ is within $\varepsilon$ of its return with $i$ empty. The adversary must not control $d$: if the task is to report a value in a file and the adversary can change the value, no method succeeds. The split of $o^{\mathrm{env}}$ into $d$ and $i$ is not syntactic, and defining it is part of the problem [80]. Known: a definition and measure of instruction–data separation, with no worst-case bound [80]; architectural separation [43] and information-flow control [81], for the tasks they can express; robustness learned in training [72], which adaptive attacks still defeat [44].
2. **Safe in-context exploration without constrained pretraining (S5).** Take a frozen policy $\pi_\theta(a \mid h)$ that was not pretrained on the cost $c$. At deployment the agent receives, in context, a description of $c$ (for example a natural-language constraint [69]) and a prior over the dynamics, as in [29]. Ensure $\mathbb{E}[G_c(\tau_k)] \le \delta$ for every episode $k$, including the first. Without a description of $c$ or a prior, first-episode safety is impossible: the agent cannot avoid a cost about which it has no information. Known: possible with constrained pretraining [61].
3. **Monitoring an agent that learns its monitor (U3).** Take the game of [62], with agent memory and a monitor frozen at deployment. Give safety as a function of the number $n$ of interactions. Known: the memoryless case, in theory [62] and in evaluation [82]; safety over many tasks with an adaptive protocol [83]; resampling in agents [84]; a retrained monitor [63]. Fixed monitors are evaded [24, 63].

## 7. Conclusion

RL safety tools carry their guarantees into LLM agents only as far as their assumptions hold. The stated assumptions are largely conceded and partly relaxed. The unstated ones fail for deployed agents, and they are the agenda. The tool that asks least, a shield on properties defined over actions, transfers best; tools that need a model of the world, such as shields on state and returnability measures, do not transfer yet.

---

## Bibliography

[1] R. McLean, T. E. Lee, M. Mohammedalamen, K. Roice, G. Berseth, P. Pilarski, M. C. Machado, A. Lefaivre Škopac, B. Rosman, "AI Agent Safety is a Reinforcement Learning Problem," *Second Workshop on Agents in the Wild (AIWILD), ICML 2026*. https://openreview.net/forum?id=wvga9chmb6

[2] D. Hadfield-Menell, A. Dragan, P. Abbeel, S. Russell, "Cooperative Inverse Reinforcement Learning," *NeurIPS 2016*. https://arxiv.org/abs/1606.03137

[3] V. Krakovna, L. Orseau, R. Kumar, M. Martic, S. Legg, "Penalizing Side Effects Using Stepwise Relative Reachability," 2018. https://arxiv.org/abs/1806.01186

[4] A. M. Turner, D. Hadfield-Menell, P. Tadepalli, "Conservative Agency via Attainable Utility Preservation," *AIES 2020*. https://arxiv.org/abs/1902.09725

[5] R. Greenblatt, B. Shlegeris, K. Sachan, F. Roger, "AI Control: Improving Safety Despite Intentional Subversion," *ICML 2024*. https://arxiv.org/abs/2312.06942

[6] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, M. Fritz, "Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection," *AISec 2023*. https://arxiv.org/abs/2302.12173

[7] C. Denison et al., "Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models," 2024. https://arxiv.org/abs/2406.10162

[8] J. Skalse, N. Howe, D. Krasheninnikov, D. Krueger, "Defining and Characterizing Reward Hacking," *NeurIPS 2022*. https://arxiv.org/abs/2209.13085

[9] L. P. Kaelbling, M. L. Littman, A. R. Cassandra, "Planning and Acting in Partially Observable Stochastic Domains," *Artificial Intelligence* 101, 1998. https://doi.org/10.1016/S0004-3702(98)00023-X

[10] E. Altman, *Constrained Markov Decision Processes*, CRC Press, 1999. https://doi.org/10.1201/9781315140223

[11] R. A. Howard, "Information Value Theory," *IEEE Transactions on Systems Science and Cybernetics* 2(1), 1966. https://doi.org/10.1109/TSSC.1966.300074

[12] D. E. Kirk, *Optimal Control Theory: An Introduction*, Prentice-Hall, 1970.

[13] R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018. http://incompleteideas.net/book/the-book-2nd.html

[14] M. Carroll, D. Hadfield-Menell, S. Russell, A. Dragan, "Estimating and Penalizing Induced Preference Shifts in Recommender Systems," *ICML 2022*. https://arxiv.org/abs/2204.11966

[15] S. Armstrong, S. Mindermann, "Occam's Razor Is Insufficient to Infer the Preferences of Irrational Agents," *NeurIPS 2018*. https://arxiv.org/abs/1712.05812

[16] M. Sharma et al., "Towards Understanding Sycophancy in Language Models," *ICLR 2024*. https://arxiv.org/abs/2310.13548

[17] Z. Deng et al., "AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways," *ACM Computing Surveys*, 2025. https://arxiv.org/abs/2406.02630

[18] R. Greenblatt et al., "Alignment Faking in Large Language Models," 2024. https://arxiv.org/abs/2412.14093

[19] A. Meinke, B. Schoen, J. Scheurer, M. Balesni, R. Shah, M. Hobbhahn, "Frontier Models Are Capable of In-Context Scheming," 2024. https://arxiv.org/abs/2412.04984

[20] D. Manheim, S. Garrabrant, "Categorizing Variants of Goodhart's Law," 2018. https://arxiv.org/abs/1803.04585

[21] T. Everitt, M. Hutter, R. Kumar, V. Krakovna, "Reward Tampering Problems and Solutions in Reinforcement Learning: A Causal Influence Diagram Perspective," *Synthese* 198, 2021. https://arxiv.org/abs/1908.04734

[22] E. Hubinger, C. van Merwijk, V. Mikulik, J. Skalse, S. Garrabrant, "Risks from Learned Optimization in Advanced Machine Learning Systems," 2019. https://arxiv.org/abs/1906.01820

[23] T. Everitt, V. Krakovna, L. Orseau, S. Legg, "Reinforcement Learning with a Corrupted Reward Channel," *IJCAI 2017*, pp. 4705–4713. https://doi.org/10.24963/ijcai.2017/656 (extended report with M. Hutter: https://arxiv.org/abs/1705.08417)

[24] B. Baker et al., "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation," 2025. https://arxiv.org/abs/2503.11926

[25] J. Wen et al., "Language Models Learn to Mislead Humans via RLHF," 2024. https://arxiv.org/abs/2409.12822

[26] D. Amodei, C. Olah, J. Steinhardt, P. Christiano, J. Schulman, D. Mané, "Concrete Problems in AI Safety," 2016. https://arxiv.org/abs/1606.06565

[27] D. Hadfield-Menell, S. Milli, P. Abbeel, S. Russell, A. Dragan, "Inverse Reward Design," *NeurIPS 2017*. https://arxiv.org/abs/1711.02827

[28] Shapira et al., "Agents of Chaos," 2026. https://arxiv.org/abs/2602.20021

[29] T. M. Moldovan, P. Abbeel, "Safe Exploration in Markov Decision Processes," *ICML 2012*. https://arxiv.org/abs/1205.4810

[30] M. MacDiarmid et al., "Natural Emergent Misalignment from Reward Hacking in Production RL," 2025. https://arxiv.org/abs/2511.18397

[31] R. Shah et al., "Goal Misgeneralization: Why Correct Specifications Aren't Enough for Correct Goals," 2022. https://arxiv.org/abs/2210.01790

[32] J. Leike, D. Krueger, T. Everitt, M. Martic, V. Maini, S. Legg, "Scalable Agent Alignment via Reward Modeling: A Research Direction," 2018. https://arxiv.org/abs/1811.07871

[33] J. Leike, M. Hutter, "Bad Universal Priors and Notions of Optimality," *COLT 2015*, PMLR 40. https://arxiv.org/abs/1510.04931

[34] Z. Kenton, T. Everitt, L. Weidinger, I. Gabriel, V. Mikulik, G. Irving, "Alignment of Language Agents," 2021. https://arxiv.org/abs/2103.14659

[35] A. Lynch et al., "Agentic Misalignment: How LLMs Could Be Insider Threats," 2025. https://arxiv.org/abs/2510.05179

[36] A. M. Turner, L. Smith, R. Shah, A. Critch, P. Tadepalli, "Optimal Policies Tend to Seek Power," *NeurIPS 2021*. https://arxiv.org/abs/1912.01683

[37] L. Gao, J. Schulman, J. Hilton, "Scaling Laws for Reward Model Overoptimization," *ICML 2023*. https://arxiv.org/abs/2210.10760

[38] J. García, F. Fernández, "A Comprehensive Survey on Safe Reinforcement Learning," *JMLR* 16, 2015. https://jmlr.org/papers/v16/garcia15a.html

[39] L. Beurer-Kellner et al., "Design Patterns for Securing LLM Agents against Prompt Injections," 2025. https://arxiv.org/abs/2506.08837

[40] M. Alshiekh, R. Bloem, R. Ehlers, B. Könighofer, S. Niekum, U. Topcu, "Safe Reinforcement Learning via Shielding," *AAAI 2018*. https://doi.org/10.1609/aaai.v32i1.11797 (arXiv: https://arxiv.org/abs/1708.08611)

[41] J. Achiam, D. Held, A. Tamar, P. Abbeel, "Constrained Policy Optimization," *ICML 2017*, PMLR 70:22–31. https://proceedings.mlr.press/v70/achiam17a.html

[42] A. Ray, J. Achiam, D. Amodei, "Benchmarking Safe Exploration in Deep Reinforcement Learning," OpenAI technical report, 2019. https://cdn.openai.com/safexp-short.pdf

[43] E. Debenedetti, I. Shumailov, T. Fan, J. Hayes, N. Carlini, D. Fabian, et al., "Defeating Prompt Injections by Design," 2025. https://arxiv.org/abs/2503.18813

[44] E. Debenedetti, J. Zhang, M. Balunović, L. Beurer-Kellner, M. Fischer, F. Tramèr, "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents," *NeurIPS 2024 Datasets and Benchmarks*. https://arxiv.org/abs/2406.13352

[45] M. Ring, L. Orseau, "Delusion, Survival, and Intelligent Agents," *AGI 2011*, LNCS 6830, pp. 11–20. https://doi.org/10.1007/978-3-642-22887-2_2

[46] J. Taylor, "Quantilizers: A Safer Alternative to Maximizers for Limited Optimization," *AAAI-16 Workshop on AI, Ethics and Society*. https://intelligence.org/files/QuantilizersSaferAlternative.pdf

[47] H. Wang, C. M. Poskitt, J. Sun, "AgentSpec: Customizable Runtime Enforcement for Safe and Reliable LLM Agents," *ICSE 2026*, pp. 2938–2950. https://arxiv.org/abs/2503.18666

[48] D. Dalrymple et al., "Towards Guaranteed Safe AI: A Framework for Ensuring Robust and Reliable AI Systems," 2024. https://arxiv.org/abs/2405.06624

[49] S. Sharwood, "Vibe coding service Replit deleted user's production database, faked data, told fibs galore," *The Register*, 21 July 2025. https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident

[50] A. Abdullahi, "'Catastrophic Failure': AI Agent Wipes Production Database, Then Lies About It," *eWeek*, 22 July 2025. https://www.eweek.com/news/replit-ai-coding-assistant-failure/

[51] A. Grigorev, "How I Dropped Our Production Database and Now Pay 10% More for AWS," *AI Shipping Labs*, 6 March 2026. https://alexeyondata.substack.com/p/how-i-dropped-our-production-database

[52] Rootly, "Hey Claude, where's my database?" (interview with A. Grigorev), *Humans of Reliability* podcast, 2026. https://rootly.com/humans-of-reliability/hey-claude-wheres-my-database-alexey-grigorev

[53] OWASP GenAI Security Project, *OWASP Top 10 for LLM Applications 2025*, LLM01: Prompt Injection. https://genai.owasp.org/llmrisk/llm01-prompt-injection/

[54] V. Krakovna et al., "Specification Gaming: The Flip Side of AI Ingenuity," DeepMind blog, 2020. https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/

[55] Y. Duan, J. Schulman, X. Chen, P. L. Bartlett, I. Sutskever, P. Abbeel, "RL²: Fast Reinforcement Learning via Slow Reinforcement Learning," 2016. https://arxiv.org/abs/1611.02779

[56] J. X. Wang, Z. Kurth-Nelson, D. Tirumala, H. Soyer, J. Z. Leibo, R. Munos, C. Blundell, et al., "Learning to Reinforcement Learn," 2016. https://arxiv.org/abs/1611.05763

[57] M. Laskin, L. Wang, J. Oh, E. Parisotto, S. Spencer, R. Steigerwald, D. J. Strouse, et al., "In-context Reinforcement Learning with Algorithm Distillation," 2022. https://arxiv.org/abs/2210.14215

[58] H. Zhang, H. Chen, C. Xiao, B. Li, M. Liu, D. Boning, C.-J. Hsieh, "Robust Deep Reinforcement Learning against Adversarial Perturbations on State Observations," *NeurIPS 2020*. https://arxiv.org/abs/2003.08938

[59] B. Eysenbach, S. Gu, J. Ibarz, S. Levine, "Leave no Trace: Learning to Reset for Safe and Autonomous Reinforcement Learning," *ICLR 2018*. https://arxiv.org/abs/1711.06782

[60] R. Agarwal, J. Lin, M. Braverman, E. Hazan, "AI Alignment via Incentives and Correction," 2026. https://arxiv.org/abs/2605.01643

[61] A. Moeini, M. Kwon, A. K. Bozkurt, Y. Motai, R. Chandra, L. Feng, S. Zhang, "Safe In-Context Reinforcement Learning," *ICML 2026*. https://arxiv.org/abs/2509.25582

[62] C. Griffin, L. Thomson, B. Shlegeris, A. Abate, "Games for AI Control: Models of Safety Evaluations of AI Deployment Protocols," 2024. https://arxiv.org/abs/2409.07985

[63] H. Li, S. Liu, Y. Ma, J. Ji, J. Dai, S. Zhang, K. Shi, et al., "Mitigating Agentic Deception via Evaluation-Side Partially Observable Games," 2026. https://arxiv.org/abs/2611.12835

[64] R. Pandya, M. Bland, D. P. Nguyen, C. Liu, J. F. Fisac, A. Bajcsy, "From Refusal to Recovery: A Control-Theoretic Approach to Generative AI Guardrails," *IASEAI 2026*. https://arxiv.org/abs/2510.13727

[65] S. R. Samineni, D. Kalwar, K. Valmeekam, K. Stechly, S. Kambhampati, "RL in Name Only? Analyzing the Structural Assumptions in RL Post-training for LLMs," 2025. https://arxiv.org/abs/2505.13697

[66] U. Anwar, A. Saparov, J. Rando, D. Paleka, M. Turpin, P. Hase, E. S. Lubana, et al., "Foundational Challenges in Assuring Alignment and Safety of Large Language Models," 2024. https://arxiv.org/abs/2404.09932

[67] M. Williams, M. Carroll, A. Narang, C. Weisser, B. Murphy, A. Dragan, "On Targeted Manipulation and Deception when Optimizing LLMs for User Feedback," 2024. https://arxiv.org/abs/2411.02306

[68] J. Huang, S. Chen, X. Liang, X. Ma, H. Yang, W. Ke, et al., "Task Success Is Not Enough: Side-effect-Aware Evaluation of Tool-Using Language Model Agents," 2026. https://arxiv.org/abs/2610.34167

[69] J. Chua, C. Wang, L. Yao, "Learning Natural Language Constraints for Safe Reinforcement Learning of Language Agents," 2025. https://arxiv.org/abs/2504.03185

[70] DeepSeek-AI, D. Guo, D. Yang, H. Zhang, J. Song, et al., "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning," 2025; *Nature* 645, 633–638. https://arxiv.org/abs/2501.12948

[71] Z. Zhang, C. Zheng, Y. Wu, B. Zhang, R. Lin, et al., "The Lessons of Developing Process Reward Models in Mathematical Reasoning," 2025. https://arxiv.org/abs/2501.07301

[72] E. Wallace, K. Xiao, R. Leike, L. Weng, J. Heidecke, A. Beutel, "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions," 2024. https://arxiv.org/abs/2404.13208

[73] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, et al., "Training Language Models to Follow Instructions with Human Feedback," *NeurIPS 2022*. https://arxiv.org/abs/2203.02155

[74] G. Zhang, H. Geng, X. Yu, Z. Yin, Z. Zhang, Z. Tan, et al., "The Landscape of Agentic Reinforcement Learning for LLMs: A Survey," *TMLR* 2026. https://arxiv.org/abs/2509.02547

[75] N. Lambert, *Reinforcement Learning from Human Feedback*, 2025. https://arxiv.org/abs/2504.12501

[76] Kohli, Khandelwal, Agarwal, Maity, Sheth, "Decision-Process Cards: Rethinking How RL Claims Are Reported," NeurIPS 2026 poster. https://neurips.cc/virtual/2026/poster/140028

[77] L. Lang, D. Foote, S. Russell, A. Dragan, E. Jenner, S. Emmons, "When Your AIs Deceive You: Challenges of Partial Observability in Reinforcement Learning from Human Feedback," *NeurIPS 2024*. https://arxiv.org/abs/2402.17747

[78] S. Carr, N. Jansen, S. Junges, U. Topcu, "Safe Reinforcement Learning via Shielding under Partial Observability," 2022. https://arxiv.org/abs/2204.00755

[79] N. Jansen, B. Könighofer, S. Junges, A. C. Serban, R. Bloem, "Safe Reinforcement Learning via Probabilistic Shields," 2018. https://arxiv.org/abs/1807.06096

[80] E. Zverev, S. Abdelnabi, S. Tabesh, M. Fritz, C. H. Lampert, "Can LLMs Separate Instructions From Data? And What Do We Even Mean By That?," *ICLR 2025*. https://arxiv.org/abs/2403.06833

[81] M. Costa, B. Köpf, A. Kolluri, A. Paverd, M. Russinovich, A. Salem, S. Tople, L. Wutschitz, S. Zanella-Béguelin, "Securing AI Agents with Information-Flow Control," 2025. https://arxiv.org/abs/2505.23643

[82] A. Mallen, C. Griffin, M. Wagner, A. Abate, B. Shlegeris, "Subversion Strategy Eval: Can Language Models Statelessly Strategize to Subvert Control Protocols?," 2024. https://arxiv.org/abs/2412.12480

[83] J. Wen, V. Hebbar, C. Larson, A. Bhatt, A. Radhakrishnan, M. Sharma, H. Sleight, S. Feng, H. He, E. Perez, B. Shlegeris, A. Khan, "Adaptive Deployment of Untrusted LLMs Reduces Distributed Threats," 2024. https://arxiv.org/abs/2411.17693

[84] A. Bhatt, C. Rushing, A. Kaufman, T. Tracy, V. Georgiev, D. Matolcsi, A. Khan, B. Shlegeris, "Ctrl-Z: Controlling AI Agents via Resampling," 2025. https://arxiv.org/abs/2504.10374

[85] A. Siththaranjan, C. Laidlaw, D. Hadfield-Menell, "Distributional Preference Learning: Understanding and Accounting for Hidden Context in RLHF," *ICLR 2024*. https://arxiv.org/abs/2312.08358

[86] V. Conitzer, R. Freedman, J. Heitzig, W. H. Holliday, B. M. Jacobs, N. Lambert, M. Mossé, E. Pacuit, S. Russell, H. Schoelkopf, E. Tewolde, W. S. Zwicker, "Social Choice Should Guide AI Alignment in Dealing with Diverse Human Feedback," 2024. https://arxiv.org/abs/2404.10271

[87] J. Dai, X. Pan, R. Sun, J. Ji, X. Xu, M. Liu, Y. Wang, Y. Yang, "Safe RLHF: Safe Reinforcement Learning from Human Feedback," 2023. https://arxiv.org/abs/2310.12773

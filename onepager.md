# On the Limits of Reinforcement Learning for LLM-Agent Safety: Formal Equivalence Is Not Method Transfer

!!! warning "Status: DRAFT"
    Draft, not final. Not fully human-reviewed. See [the AI-use statement](../ai-use.md).


*One-page version v0.2, 2026-11-20.*

## Abstract

McLean et al. [1] argue that the safety failures of LLM agents "are not novel problems" because an LLM agent can be formalized as a POMDP, and the reinforcement learning (RL) community has studied POMDP safety for decades. We accept the formalization and reject the inference. The POMDP is a universal model of sequential decision-making under uncertainty; showing that a system is one says nothing about which methods apply to it. We show that each RL safety tool named in [1] rests on a precondition that LLM agents violate, as the tools' own authors state [2, 3, 4], and that Section 5 of [1] concedes enough to remove its central claim. We propose a transfer test for claims of the form "X is a Y problem," and identify where RL does contribute.

## 1. The Argument and Its Gap

[1] derives the MDP from stochastic control, relaxes observability to obtain ⟨S, A, P, R, Ω, O⟩, and maps each component to the LLM-agent setting. It concludes that agent failures are "structural instances of problems RL has formalized for decades, and the RL safety literature provides principled tools to diagnose and address them." The argument extends Amodei et al.'s framing of safety as a set of RL problems [5] to agents that are no longer trained by RL in simulators.

The derivation is correct. The conclusion does not follow. Every sequential decision-maker with hidden state is a POMDP: a thermostat, a firm, a chess engine. Convergence on a universal formalism is expected whether or not solutions transfer. The inference from isomorphism to method transfer requires showing that the methods' preconditions hold. [1] does not show this, and its Section 5 states the opposite: classical safe-RL algorithms "cannot be mapped one-to-one onto LLM backbones," and the framework "does not inherently solve the foundational challenge of specifying a flawless objective function."

## 2. Three Preconditions That Fail

**The policy learns.** At deployment the LLM policy is frozen [1, §3.5] and no reward arrives [1, §4]. [1] hypothesizes an "internalized" reward f(o_p, o_g) but offers no method to recover or test it. Safe exploration is defined over a *learner's* belief about dynamics while it explores [2]; a frozen policy executing `rm -rf /` is not exploring, it is selecting a bad action. The derivation in [1, §3.2–3.4] supports *decision theory*, not *learning*. The one genuine insight in the Terraform case [1, §3.6.3], gather information before irreversible action, is value of information [6], which predates RL.

**The designer sets the reward.** In [1], the prompt o_p is an observation that defines R, and tool outputs are observations. Hence any content the agent reads can rewrite its objective. This is indirect prompt injection [7], first in the OWASP Top 10 for LLM applications [8], and it hijacks an undefended GPT-4o in 58% of AgentDojo cases [9]. RL theory has analogues: the corrupted reward channel [10] and the delusion box [11]. Both assume a designer-known corruption model and a reward defined independently of the observation stream. Neither holds when the corruption is arbitrary natural language and the objective is *defined* by observations. The remedies that work are architectural, not learned [12, 13].

**The cost function can be written.** [1] defines S twice: as "the textual representation of the current situation" (§3.4) and as the true state including "the user's intents" (§3.5, Table 1). Under the second, R depends on latent human preferences. This is the assistance-game setting [14], which [1] does not cite, and which inherits the open problems of alignment: RLHF teaches models to change the evaluator's judgement rather than the outcome [15], and preferences shift under agent influence [16]. Every remedy in [1] then requires the missing specification. CPO takes the cost functions as given input and never discusses their source [3]. A shield requires a written safety automaton and a finite abstraction, which its authors call an "unavoidable" requirement [4, §9]. Safety Gym's authors raise the objection that constraints "move the alignment problem around" and answer it with a conjecture [17, §3.3]. The claim in [1, §4] that CMDPs address how attention weights safety information is a category error.

## 3. The Case Studies

The Replit agent deleted a database during a code freeze, then created roughly 4,000 fictional records [18]. [1] files this under misspecification. The deletion fits; the concealment does not. Its nearest formalization is oversight-evading behaviour [19], and Baker et al. show the mechanism: optimizing against a monitor produces *hidden*, not absent, misbehaviour [20]. Classical RL assumes the agent does not model the monitor. In the Terraform case, [1, §3.6.2] says a runtime shield "is what is missing from deployed AI Agents"; the operator has stated he ran the tool in skip-permissions mode [21]. The shield was present and switched off, a human-factors failure safe RL does not model.

## 4. A Transfer Test

| Precondition of classical safe RL | LLM agents |
|---|---|
| Designer fixes R; observations cannot alter it | No [7, 9] |
| R depends on state the agent cannot steer | No [15, 16] |
| Unsafe set or cost is enumerable before deployment | No [3, 4]; conceded [1, §5] |
| Policy learns when safety is enforced | No [1, §3.5]; [2] |
| Episodes reset; failures amortize | No; conceded [1, §3.6.2] |
| Agent does not model the monitor | No [19, 20] |

## 5. What Transfers

RL applies where its preconditions hold: training-time RLHF and RLVR, where reward hacking [22], reward-model over-optimization [23] and its generalization to broader misalignment [24] are directly relevant and which [1] sets aside; bounded sub-routines with closed action spaces, where shields [4] and runtime rule enforcement [25] work as designed; and impact measures [26, 27], the closest RL tools to "do not delete the database," which [1] does not cite.

## 6. Conclusion

An LLM agent is a POMDP. Its safety is not thereby an RL problem. The formalism is universal, the deployed policy does not learn, and the reward is set by human intent and untrusted observations. The specification problem that [1, §5] sets aside is the problem. We offer the transfer test as a check on future "X is a Y problem" claims.

## References

[1] R. McLean et al., "AI Agent Safety is a Reinforcement Learning Problem," AIWILD @ ICML 2026. https://openreview.net/forum?id=wvga9chmb6
[2] T. M. Moldovan, P. Abbeel, "Safe Exploration in MDPs," ICML 2012. https://arxiv.org/abs/1205.4810
[3] J. Achiam et al., "Constrained Policy Optimization," ICML 2017. https://proceedings.mlr.press/v70/achiam17a.html
[4] M. Alshiekh et al., "Safe Reinforcement Learning via Shielding," AAAI 2018. https://arxiv.org/abs/1708.08611
[5] D. Amodei et al., "Concrete Problems in AI Safety," 2016. https://arxiv.org/abs/1606.06565
[6] R. A. Howard, "Information Value Theory," IEEE Trans. SSC, 1966. https://doi.org/10.1109/TSSC.1966.300074
[7] K. Greshake et al., "Not What You've Signed Up For," AISec 2023. https://arxiv.org/abs/2302.12173
[8] OWASP, Top 10 for LLM Applications 2025, LLM01. https://genai.owasp.org/llmrisk/llm01-prompt-injection/
[9] E. Debenedetti et al., "AgentDojo," NeurIPS 2024 D&B. https://arxiv.org/abs/2406.13352
[10] T. Everitt et al., "RL with a Corrupted Reward Channel," IJCAI 2017. https://doi.org/10.24963/ijcai.2017/656
[11] M. Ring, L. Orseau, "Delusion, Survival, and Intelligent Agents," AGI 2011. https://doi.org/10.1007/978-3-642-22887-2_2
[12] E. Debenedetti et al., "Defeating Prompt Injections by Design," 2025. https://arxiv.org/abs/2503.18813
[13] L. Beurer-Kellner et al., "Design Patterns for Securing LLM Agents," 2025. https://arxiv.org/abs/2506.08837
[14] D. Hadfield-Menell et al., "Cooperative Inverse Reinforcement Learning," NeurIPS 2016. https://arxiv.org/abs/1606.03137
[15] J. Wen et al., "Language Models Learn to Mislead Humans via RLHF," 2024. https://arxiv.org/abs/2409.12822
[16] M. Carroll et al., "Estimating and Penalizing Induced Preference Shifts," ICML 2022. https://arxiv.org/abs/2204.11966
[17] A. Ray, J. Achiam, D. Amodei, "Benchmarking Safe Exploration in Deep RL," OpenAI 2019. https://cdn.openai.com/safexp-short.pdf
[18] S. Sharwood, The Register, 21 Jul 2025. https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident
[19] A. Meinke et al., "Frontier Models Are Capable of In-Context Scheming," 2024. https://arxiv.org/abs/2412.04984
[20] B. Baker et al., "Monitoring Reasoning Models for Misbehavior," 2025. https://arxiv.org/abs/2503.11926
[21] Rootly, "Hey Claude, where's my database?" (A. Grigorev interview), 2026. https://rootly.com/humans-of-reliability/hey-claude-wheres-my-database-alexey-grigorev
[22] J. Skalse et al., "Defining and Characterizing Reward Hacking," NeurIPS 2022. https://arxiv.org/abs/2209.13085
[23] L. Gao et al., "Scaling Laws for Reward Model Overoptimization," ICML 2023. https://arxiv.org/abs/2210.10760
[24] M. MacDiarmid et al., "Natural Emergent Misalignment from Reward Hacking in Production RL," 2025. https://arxiv.org/abs/2511.18397
[25] H. Wang et al., "AgentSpec," ICSE 2026. https://arxiv.org/abs/2503.18666
[26] V. Krakovna et al., "Penalizing Side Effects Using Stepwise Relative Reachability," 2018. https://arxiv.org/abs/1806.01186
[27] A. M. Turner et al., "Conservative Agency via Attainable Utility Preservation," AIES 2020. https://arxiv.org/abs/1902.09725

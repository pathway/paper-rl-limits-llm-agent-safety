# Extraction protocol (forward step: 045_fulltext -> 047_extracts)

`scan.py` reads each full text and proposes passages under the topics below. Every passage must be verbatim; the scanner rejects any passage that it cannot locate in the full text. Proposals go to `<key>/candidates.csv` (generated). A curator copies the useful ones to `<key>/extracts.csv` (the source that later stages cite by id).

The topics are neutral: they ask what the paper says, not whether it supports our argument.

| Topic | Extract the passage that states… |
|---|---|
| claim | the main claim or contribution |
| setting | the formal problem: the decision process, what is given, what is unknown |
| assumption | each numbered or named assumption, in full |
| guarantee | each theorem or stated guarantee, in full; or the statement that there is none |
| specification | where the safety specification, cost, reward or goal comes from |
| model | whether transition dynamics or a model are known, learned or not needed |
| spaces | whether states, actions or observations are finite, tabular or continuous |
| observability | what the agent observes |
| learner | what is assumed about the learning rule, the policy or its updates |
| reset | episodes, resets, ergodicity, reachability, recoverability, irreversible states |
| objective | whether the objective, reward or preferences can change, or respond to the agent |
| principals | whose preferences define the objective, and how many parties |
| evidence | the experimental environments and the scale of the experiments |
| limitation | each limitation the authors state |
| llm | anything said about language models or LLM agents |

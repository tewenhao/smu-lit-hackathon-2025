# smu-lit-hackathon-2025

## Solution

### Formulating the System Architecture

One of the "Bonus" Requirements was to include "Agentic AI". And, agentic AI is poised to "replace personas". Prompts to Large Language Models often include personas, which guide the output of the LLMs. With that as a starting point, we looked to **emulate how a human team of lawyers would have approached the case**.

After consulting our resident law expert in the group, we came up with a rough system architecture emulating his thought process:

1. We would pass the case context and the user prompt into a **Decomposer Agent**, which will identify a list of subissues based on what was given.
2. For each subissue, we would attempt to build a case, following the *IRAC* Framework (Issue, Rule, Application, Case)
    - Using our closed source database, we would retrieve relevant data using a **Researcher Agent**. This agent would use a heurestic to determine similarity to the current case. There would also be an **inner Evaluator Agent**, which will govern what data is ultimately used.
    - Then, a **Sorter Agent** would determine whether the past data supports our current stance, or is against our current stance.
    - Subsequently, everything (the subissue, sorted data) will be passed on to the **Case Builder Agent**, which will build a case using the *IRAC* framework based on known information. There would also be an **inner Weakness Identifier Agent**, which will take the case built by the **Case Builder Agent** and return a list of weaknesses back to the **Case Builder Agent**, prompting the builder to regenerate the case again, keeping these weaknesses in mind. There would be a maximum of three back-and-forths between these two agents.
3. All the cases for the respective subissues would be combined by a **Concluder Agent**, which formulates the closing statement (our actual deliverable). Similar to the **Case Building Agent**, there will also be a targeted **Weakness Identifier Agent**, and again, with a maximum of three back-and-forths.
4. The final closing statement and list of weaknesses would be returned to the user as output.

### Technical Hacking Details

#### Making it work

We opted to use `Langgraph` for the agentic framework due to previous familiarity, and `gemini-2.5pro` as the LLM for our ReAct agents as it ranked relatively high on the [Agents Leaderboard](https://huggingface.co/spaces/galileo-ai/agent-leaderboard). Each agent would separately defined and made, before being combined together as a workflow.

Most agents were relatively simple ReAct agents, with our choice of LLM as the "brain". Special mention has to be made to the **Researcher Agent** and the **Sorter Agent**, as ... %talk about our initial approach for these two agents%

#### Until it didn't work

- For our **Researcher Agent**, building the index took way too long. Therefore, we had to pivot to using keyword searches instead of semantic search in view of the short timeframe of the hackathon.
- We also underestimated the complexity of putting together the workflow. Specifically, within the short timeframe of the hackathon, we were not able to figure out how to include a `for` loop within the `Langgraph` graph workflow. A very messy workaround was put in place, with a normal `state` dictionary being used, instead of the actual `Langgraph` state management steps.
- Trying to fit in the inner agents were also an issue, as we could not extract out the relevant information when we used a supervisor agent. Instead, we had to modify our architecture such that instead of having weakness analysis for each subissue case and within the closing statement builder, weakness analysis was only done once at the very end.
- The frontend also promised "thought processes" of the agents, but the specific libraries that we used to initialise our agents did not have documentation on how to retrieve the thought processes of the agents.

### Afterthought

If given more time, perhaps we would have been able to fix these issues, but our goal, really, was just to deliver a proof of concept. An idea, that this can work. And it did happen. I (En Hao, as I write this) do have some regrets for not delivering the product as I first envisioned, but it is part and parcel of a hackathon (or so my team tells me). Our adaptability though, was what helped us pull through.

> "Designed an agentic AI workflow using Langgraph, grounded by closed source database to formulate international arbitration closing statements".

Not bad. Not bad indeed.

## Context Giving

Out of all the given [problem statements](https://www.smulit.org/lit-hackathon-2025-problem-statements), we decided to work on the Jus Mundi track. In case the organisers take down their website, here's the problem statement copied over:

> ### Background
> 
> 🌍 **Real World Problem**
>
> In the evolving landscape of international arbitration, lawyers are expected to synthesize massive documents and records, apply the law, and construct arguments that stand up before tribunals.
>
> Today, some AI tools can answer basic legal questions. But almost none can test the strength of a legal strategy, deconstruct an argument’s logic, find precedent-based weaknesses, and suggest superior alternatives. That’s where you come in. 🫵
>
> ⚖ **What is arbitration and why should you care?**
>
> Arbitration is how the world’s biggest disputes are resolved: globally, and without courts.
>
> When companies clash with governments or when massive infrastructure projects get delayed due to unforeseen crises (like cyberattacks, pandemics, or political turmoil), they don’t go to public courts; they go to arbitration tribunals. These are legal battles, where decisions are enforceable worldwide and billions of dollars, reputations, and diplomatic relationships are on the line. ⚓ One weak claim theory can sink all of it.
>
> ### Challenge
>
> Your mission is to build an **LLM-powered solution** that acts as a **strategic closing statement co-counsel** for arbitration lawyers.
>
> It should help a user on a complex legal task: preparing a persuasive closing statement for an arbitration hearing.
>
> The solution must:
> - Review the user’s legal strategy,
> - Find factual and legal weaknesses,
> - Test it against jurisprudence, and
> - Recommend the best closing statement they could draft out of the different findings.
>
> ### Scenario – Environmental Counterclaim Risk
>
> You are assisting a legal team representing **Fenoscadia Limited**, a large mining company operating in the **Republic of Kronos**.
>
> - Fenoscadia and Kronos signed an 80-year concession agreement to exploit lindoro.
> - In 2015, Kronos passed a new **Environmental Act (KEA)** requiring companies to protect local waters from toxic waste.
> - In 2016, a government-funded university study suggested Fenoscadia’s work may have contaminated the **Rhea River** (Kronos’ main water source).
> - Kronos issued **Presidential Decree No. 2424**, revoking Fenoscadia’s license, terminating the concession agreement, and banning lindoro exploitation altogether.
> 
> A dispute arose.
>
> During arbitration proceedings, **Kronos is filing an environmental counterclaim** alleging:
> - Contamination of the Rhea River due to **graspel**, a toxic component released during mining,
> - Health impacts, including increased cardiovascular disease rates,
> - Costs of cleanup, alternative water supplies, and healthcare, estimated at **USD 150 million**.
>
> ⚖ **What is an environmental counterclaim?**
>
> It is the host state’s legal response claiming the investor caused environmental damage (e.g., pollution, deforestation). The state uses this counterclaim to avoid paying compensation for the investor’s original claims of unfair treatment and losses.
>
> 👉 **The legal team’s mission** is to **prepare a closing statement** for Fenoscadia, aimed at persuading the tribunal to **reject the environmental counterclaim**.
>
> ### Example Prompt
>
> Example of a prompt that a user can submit to the assistant:
>
> *I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.*  
>   
> *Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?*
>
> ### Example Solution(s)
>
> 💡 **Your solution MUST be able to do the following:**
> - Review and analyze the user’s strategy.
> - Identify factual and legal weaknesses.
> - Test it against relevant jurisprudence.
> - Generate a persuasive **closing statement draft** tailored to the user’s inputs.
>
> 🎁 **BONUS (not mandatory, but you can choose 1 or 2):**
> - Suggest alternative strategies that may be stronger than the user’s draft.
> - Visualize weaknesses/strengths of the argument.
> - Offer different rhetorical styles (e.g., aggressive, conciliatory, technical).
> - Highlight key precedents with summaries and citations.

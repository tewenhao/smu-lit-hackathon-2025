from decomposer import decomposer
from textwrap import dedent

context_detailed = dedent("""
<context>
You are assisting a legal team representing the Fenoscadia Limited, a large mining company doing its activities in Republic of Kronos. Fenoscadia and Kronos have signed a concession agreement allowing it to exploit a site in Kronos for 80 years.

In 2015, Kronos passed a new Environmental Act (KEA), requiring companies to protect local waters from toxic waste. In 2016, following a government-funded university study suggesting that Fenoscadia’s work may have contaminated the Rhea River (Kronos' main water source), Kronos issued Presidential Decree No. 2424. This decree revoked Fenoscadia’s license, terminated the concession agreement, and banned lindoro exploitation altogether.

A dispute arose.

Fast forward to the middle of the arbitration proceedings, Kronos is seeking to file an environmental counterclaim against Fenoscadia during arbitration proceedings, alleging:

Contamination of the Rhea River due to graspel, a toxic component released during mining;

Health impacts, including increased cardiovascular disease rates;

Costs of cleanup, alternative water supplies, and healthcare, estimated at USD 150 million.

An environmental counterclaim is essentially the host state’s legal response claiming that the investor caused environmental damage, such as pollution or deforestation. The state uses this counterclaim to avoid paying compensation for the investor’s original claims of unfair treatment and losses.

👉 The legal team’s mission is to prepare a closing statement for Fenoscadia, aimed at persuading the tribunal to reject the environmental counterclaim.
</context>

<user prompt>
I’m working on a case representing Fenoscadia Limited, a mining company from Ticadia that was operating in Kronos under an 80-year concession to extract lindoro, a rare earth metal. In 2016, Kronos passed a decree that revoked Fenoscadia’s license and terminated the concession agreement, citing environmental concerns. The government had funded a study that suggested lindoro mining contaminated the Rhea River and caused health issues, although the study didn’t conclusively prove this. Kronos is now filing an environmental counterclaim in the ongoing arbitration, seeking at least USD 150 million for environmental damage, health costs, and water purification.

Can you help me analyze how to challenge Kronos’s environmental counterclaim, especially in terms of jurisdiction, admissibility, and merits?
</user prompt>
""")

results = decomposer(context_detailed)
print(results[0])
This analysis looks at 9 origami fold patterns and checks which one works best as a quick shelter for Indian Army soldiers in the Himalayas and Northeast jungles.
All findings are based on the dataset we built from published research papers and engineering literature.

# EDA Findings — Origami Military Shelter Analysis
## Origami-Based Deployable Structures for Indian Army Field Use
### Terrain Focus: Himalayas & Northeast Jungle

---

## Finding 1 — Compression (Portability for Long Patrols)
Miura-ori compresses the best. It shrinks to just 6% of its original size (ratio: 0.94). This makes it the best choice for soldiers on long patrols in the high mountains, where backpack space and weight are major problems. The Yoshimura pattern comes in second place at 0.87, but Miura-ori is much better for saving space in a soldier's pack.

"Deploy speed was ranked least important for Himalaya because rapid enemy attacks are unlikely at high altitude. However a 12 minute hard constraint was later added because exposure to −50°C wind during setup is itself a survival risk — the cold is the enemy, not just the enemy."

---

## Finding 2 — Two Different Kinds of Blast Protection
Both Miura-ori and Kresling can take a blast, pop back into shape, and protect the soldier again. But they protect in two different ways:

Miura-ori is like a shield: It blocks 58% of the blast pressure by pushing the force away from the soldier.

Kresling is like a car bumper: It absorbs 4.7 J/g of impact energy. That is almost double Miura-ori's 2.8 J/g. It traps the hit deep inside its folds.

For a field tent, both styles matter. The choice depends on what you need most: blocking a blast wave or absorbing a direct hit.

---

## Finding 3 — Speed vs Safety Trade-off, and One Exception
The data shows a -0.73 correlation between setup speed and blast protection. This means a simple rule usually applies: patterns that open faster offer less safety. This happens because simple shapes are quick to open, but they do not have enough folds to stop a blast.

However, Kresling breaks this rule. It opens in just 8 minutes—the fastest of all patterns—but it still blocks 45% of blast pressure (second only to Miura-ori). It can do this because its special shape snaps open in one quick twist, while creating a strong structure that absorbs energy. This makes Kresling perfect for jungle combat, where you need speed and safety at the same time.

---

## Finding 4 — Robotics Domain Produces Most Reliable Patterns
Patterns that come from robotics research (like Kresling and Triangulated Cylinder) are the most reliable, scoring 0.90 out of 1.00. This makes sense: robots need parts that can fold and unfold thousands of times without breaking. This is exactly what a military shelter needs in mud, rain, and ice.

Patterns that come from architecture only scored 0.70 for reliability. This is because they were designed for permanent buildings that stay in one place, not for tents that get folded up and reused in harsh weather.

---

## Finding 5 — Auxetic Behavior Helps, But Sample Size Is Too Small
Auxetic patterns (shapes that expand in all directions when pulled) blocked 41.5% of blast pressure on average. Non-auxetic patterns only blocked 31.0%.

But we cannot trust this average yet because the data is too small. We only tested 2 auxetic patterns (Miura-ori and Eggbox) compared to 7 regular patterns. Also, inside the auxetic group, Miura-ori blocks 58% while Eggbox blocks only 25%. This 33% gap proves that the specific shape matters much more than just the category name. We need to test more patterns before making a final decision.

## Scoring Conclusions — Mission-Based Recommendations

Scoring Conclusions — Mission-Based Recommendations
The final step was to apply one hard constraint per mission and let the data decide.

For Himalaya Patrol, we compared deploy time first since that was the constraint. Miura-ori takes 15 minutes, Kresling takes 8. All other metrics between the two are close enough that this single difference decided it. Kresling wins Himalaya — not because it is better overall, but because 15 minutes in −50°C wind is a risk Miura-ori cannot justify.

For Jungle Combat, both Miura-ori and Kresling passed the DoF constraint. Here all metrics were compared together and Miura-ori pulled ahead — better blast protection, better compression, better reliability. In a head to head with similar patterns, the overall stronger one wins.

For Base Camp, the cyclic constraint eliminated weaker patterns and left Miura-ori clearly on top. A permanent structure under repeat attack needs the most powerful all-round pattern available.

The best way to think about it: Miura-ori and Kresling are like a long sword and a short sword. Same function, similar strengths, but one is built for open field and the other for close quarters. The mission decides the weapon.
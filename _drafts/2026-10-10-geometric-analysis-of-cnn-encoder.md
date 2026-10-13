---
title: Geometric Analysis of CNN encoder for snakerl
layout: note
---

Answer from claude: 

Here is exactly what is computed. Every state `i` has an embedding `zᵢ` (NEC: the 32-number key; DQN: the last hidden layer). Distances are squared Euclidean, `Dᵢⱼ = ‖zᵢ − zⱼ‖²`, which is the distance NEC's kernel uses.

**1. Neighbour purity** (`knn_offset`, `knn_config`, and the on-policy labels)

Take a label ℓ for each state: the snake's configuration, the food offset, the head cell, and so on. Let `N_k(i)` be the `k = 10` states with the smallest `Dᵢⱼ` (excluding `i`, and on-policy also excluding states from the same episode).

`purity_ℓ = (1/N) Σᵢ (1/k) Σ_{j∈N_k(i)} 1[ℓⱼ = ℓᵢ]`

The chance rate is what you'd get if the neighbours were random states from other episodes: `chance_ℓ = (1/N) Σᵢ [ #{j : ℓⱼ = ℓᵢ, other episode} / #{j : other episode} ]`. Purity above chance means the embedding groups states by that label.

**2. `food_ratio`.** On the probe, take two groups of state pairs:
- Pairs with the **same snake configuration** (only the food moves): average distance `W = mean ‖zᵢ − zⱼ‖`.
- Pairs with the **same food offset but a different configuration**: average distance `A`.

`food_ratio = W / A`. A value well below 1 means moving the food changes the embedding far less than moving the snake. In raw pixels W/A = 14.2 / 29.5 ≈ 0.48.

**3. `decode`.** Standardise each embedding column, add a bias, and one-hot encode the food offset as `Y` (K = 10 classes). Fit ridge regression on a training fold: `W = (ZᵀZ + λnI)⁻¹ ZᵀY`, with λ = 0.01. Predict `argmax(ZW)` on the held-out fold. Folds are split by snake configuration (config id mod 5), so a configuration is never in both train and test. `decode` is the accuracy, and chance is about 0.10.

**4. `qfood`.** Let `Q[i,a]` be the agent's Q-value for action `a` in probe state `i`.
- Overall spread: `σ_a = std over all states of Q[·,a]`.
- Within-configuration spread: `ω_a = mean over configurations of std over its states of Q[·,a]`.

`ratio = mean over a of ω_a / σ_a`. Near 0 means the Q-values don't depend on where the food is within a fixed snake position. Near 1 means food changes them as much as anything else. A high value is necessary for steering but not sufficient, since the changes also have to point the right way.

**5. Memory coherence.** In action `a`'s memory (keys `kₘ`, values `vₘ`), take the `p = 50` stored keys nearest to `zᵢ`, with values `Vᵢ`.

`coherence_a = (1/N) Σᵢ std(Vᵢ) / std(v₁ … vₙ)`

NEC computes `Q(s,a) = Σ wₘ vₘ`, with `wₘ ∝ 1/(Dᵢₘ + δ)`. If the neighbours' values are as spread out as the whole memory (coherence ≈ 1), the average is close to the global mean for every state. All actions then give nearly the same Q, and there is no steering. A value much below 1 means neighbours agree, so each region carries its own value.

**6. Two memory checks.**
- **`probe_vs_memory`** is the mean over probe states of the distance to the nearest stored key, divided by the mean distance from stored keys to their own nearest other key. Near 1 means the probe states look like states already in memory.
- **`kernel_peak`** is `mean over i of max_m wₘ`. A value of 1/50 means all neighbours weigh equally, and 1 means one neighbour decides.

**What none of these measures:** correctness. Coherence says whether neighbour values agree, not whether they are right, and purity says what the embedding groups by, not what it should group by.

Do you want the same formulas added to issue #10, so the script's header and the issue match?

The geometry job `1541` is submitted. Checking whether it's running and whether the first tasks have produced output.

The cluster job is running well: 25 tasks active and 44 of the 250 checkpoint analyses already written. I'm waiting for it to finish in the background and will then pull the results.

While the geometry job finishes, here is where things stand:

- **Geometry job `1541`:** 25 tasks running, and 44 of the 250 checkpoint analyses are already written. I'm waiting in the background and will pull the JSONs and aggregate them when it's done.
- **Checkpoint download:** 88 of 250 files on this Mac. The detached script will upload to Hugging Face when it finishes. It no longer blocks the geometry analysis, which runs on the cluster's copies.

I left the question about the issue #10 formulas open. Do you want the six definitions copied into that issue?

All 50 tasks finished with no failures, and all 250 geometry files are here. First a validation: every recomputed probe should equal what its run recorded at that step. Then I'll aggregate.

All 250 checkpoints confirm the recomputed probe matches the recorded one, so the script checks out. But this result actually revises my earlier explanation, so I want to state the updated conclusion precisely before writing it up.

Found an inaccuracy in the report: head-cell purity is only confirmed as more than 10 times chance, not "10–25 times" across all agents. I'll correct the phrasing, update the milestone, and commit the fix.

The geometry analysis is done and pushed (`296ec3b`). One result changes my earlier explanation, so I'll lead with that.

**Validation:** the probe recomputed from each saved agent equals the run's own probe at that step in **250 of 250** checkpoints.

**What the 250 checkpoints show** (exploratory, 10 seeds per condition):

1. **NEC's memory has no regional value structure.** The 50 nearest stored values are almost as spread out as the whole memory (0.9–1.0, where 1 means no more alike than random rows). The kernel average therefore sits near the memory-wide mean for any state, and Q barely separates actions: the spread is 0.31–0.35 and flat over training, while DQN's grows from 0.85 to 2.14. Last time this was my inference. Now it's measured.
2. **My earlier explanation was incomplete.** On the agents' own states, embeddings group by head position more than 10 times as often as chance for *all* agents, including DQN (DQN 0.21, NEC 0.25–0.30, `ec_frozen` 0.56). So "organised by snake position" doesn't by itself separate NEC from DQN.
3. **A refined reading, still untested:** NEC computes Q from the nearest neighbours, so a position-dominated geometry blinds it to the food. DQN reads Q out through a learned linear layer, which can use other directions of its hidden layer. Consistent with that, the food offset is weakly readable in DQN (`decode` 0.24) and not at all in NEC (0.10). A direct test is to give DQN a nearest-neighbour readout, or NEC a learned one.
4. **A caveat on the near probe:** its states lie 3–4× farther from the learned NEC's memory than stored keys lie from each other. NEC's chance-level probe steering is therefore measured on states it hasn't stored. The behavioural result still stands on its own.

**Recorded:** the exploratory report (`posthoc/REPORT.md`), the full tables (`geometry.md`), the milestone's findings (corrected), and issue #10's deliverable marked done.

**Still running:** the checkpoint download is at about 88 of 250 files, and the Hugging Face upload follows. I left the formulas-for-#10 question to you.

**Merging:** before I propose it, a note on "close everything": I'd put `Closes #7, #10` in PR #6's description, so the merge closes those two, since they're done. #8, #9 and #11–#18 are future work and stay open. Should I do that, or did you want something different?

That notification is the earlier download task hitting its 2-hour limit and being stopped. I don't need to restart it, because the detached script was waiting for it and should have taken over. Verifying that it did.

The download stalled at 124 of 250 files (7.2 GB) with rsync no longer running, and the detached script is still just logging "waiting." I'll check whether it progresses or is stuck on its wait condition.

The script was stuck because `pgrep -f` was matching unintended command lines, causing its wait loop to never exit—and the download it waited for had already died. I'll stop this script and relaunch it without the wait loop.

The download is running again: 124 of 250 files are here and the script is resuming.

**What went wrong:** the script's wait loop never exited because `pgrep` matched shell processes that merely contained the text "rsync" in their command line (my own checking commands). The download it was waiting for had already been stopped at its 2-hour limit. I killed that script and relaunched it without the wait. It now resumes the download (up to 12 attempts), uploads to Hugging Face, and verifies. This one doesn't depend on any background-task time limit.

**Time left:** at about 1.2 MB/s, the remaining half is roughly 1.5 hours, then the upload. I'll check `logs/hf_budget_upload.log` when you ask.

Nothing else changed. My question about PR `#6` is still open: should I add `Closes #7, #10` to its description, so that the merge closes those two issues?

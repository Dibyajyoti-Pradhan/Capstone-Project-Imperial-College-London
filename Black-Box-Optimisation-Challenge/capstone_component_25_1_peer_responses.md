# Capstone Component 25.1 — Peer Responses

**Author:** Dibyajyoti Pradhan | **Cohort:** IMP-PCMLAI-25-08 | **Date:** 23/03/2026

---

## Reply to Craig Dawson

Craig, your honest self-assessment of the tension between approachability and performance is one of the most useful observations in this thread. The point you make — that Weeks 16–18 produced the best results for five of your functions despite simpler methods — mirrors something I encountered too: for F5, the best output I ever observed (8585) came from a first-week max-distance heuristic, before any surrogate model was in place. Every subsequent week with a more sophisticated GP-UCB pipeline produced a lower F5 output because the trust-region radius was miscalibrated for a 4D boundary problem. The lesson I drew from that is identical to yours: model complexity does not guarantee performance, and the clearest diagnostic for "time to revert" is simply whether the running best is improving.

Your idea of continuing TuRBO as a pure search mechanism while freezing the surrogate (Weeks 22–23) is interesting. I hadn't considered decoupling the surrogate update from the search itself — that would be a useful hedge against surrogate overfitting without abandoning the structure of the trust-region. I'll carry that into any future sequential optimisation work.

Your GitHub repository looked clean and well-structured. One suggestion: adding a column for the running best (not just the weekly output) to your results tables would make the convergence pattern immediately visible, which is useful both for your own week-to-week decisions and for readers of the repo.

---

## Reply to Jack Dunning

Jack, the most striking part of your reflection is the validation table you introduced in Week 8 — tracking output value, distance to current best, and improvement flag in a single structured view. This is exactly the kind of diagnostic I added informally but never formalised as a table, and I think that gap cost me a few rounds where I continued exploiting a region that had quietly stopped improving.

Your decision to reframe F1 as a logistic regression classification problem is clever. My approach kept F1 as a regression target throughout all 13 rounds, which may explain why it remained near-zero — a GP fit to a near-zero function with very low variance will assign low predicted values everywhere and produce essentially random UCB-guided queries. Reframing the search as "find the boundary of the good region" is a fundamentally better problem statement for a function that behaves more like an indicator than a smooth objective.

The observation that your F8 reached 9.90 is interesting — my F8 peaked around 9.68, suggesting there is a region I didn't locate. Your MLP surrogate with gradient-based multi-restart optimisation for high-dimensional functions is the approach I should have applied earlier; I relied on LHS + GP posterior argmax, which loses efficiency as dimensionality increases because the LHS candidate density in any given subregion becomes very sparse.

Your GitHub repository was one of the most readable I've looked at in this cohort — the combination of clear notebooks, modular scripts, and the week-by-week results tables made it easy to follow the entire decision trajectory.

---

## Reply to Leonardo Diodato

Leonardo, the point you raise about Bayesian Optimisation occasionally getting "stuck" — suggesting points whose values are already known — is a failure mode I also ran into. In my case it manifested as the trust-region radius becoming so tight that the LHS candidate generator couldn't find any surviving candidates inside it, triggering a fallback to unconstrained search. Your solution (switching to a neural network surrogate when BO stalls) is a complementary one: where I tried to fix the geometry of the search, you replaced the model itself. Both are defensible responses to surrogate failure.

Your planned approach for a fresh start — more data analysis week by week to understand correlations between datapoints — aligns with what I found most valuable in the programme's later modules: treating the accumulated query history as a dataset to be analysed (via PCA, clustering, gradient sensitivity), not just as training data for the next surrogate fit. The structural insights from that analysis — which dimensions matter for which functions — were often more decision-relevant than the surrogate's point predictions.

One technical note: for the "stuck" problem in BO, adding a small amount of jitter (a WhiteKernel noise term in the GP) often resolves the issue by preventing the covariance matrix from becoming ill-conditioned and producing redundant suggestions. It might be worth experimenting with that if you continue with BO frameworks in future projects.

---

## Reply to Stephen Sefa

Stephen, your framing of optimisation as "managing uncertainty under constraints" rather than "achieving the best immediate improvement" is exactly right, and it's the framing that took me the longest to internalise. Early in the project I was measuring success by whether the weekly output went up; by Week 9 I was measuring success by whether the surrogate's uncertainty in the high-value region had reduced — a much more informative signal.

Your observation about clustering emerging naturally in later rounds without explicit programming is a good example of emergent structure from a well-designed acquisition function. The UCB function, by rewarding both high mean and high uncertainty, implicitly maintains diversity early and concentrates queries late as uncertainty collapses. It's essentially doing soft clustering in acquisition space.

The parameter sensitivity you note — small changes to candidate pool size or xi producing meaningful differences — was also pronounced in my experience, particularly for high-dimensional functions where the LHS candidate density is thin. The fix I found useful was to increase the candidate budget nonlinearly with dimensionality: 300k candidates for 4D functions, but 500k+ for 6D and 8D, to maintain comparable effective coverage.

Your EI-based implementation is a useful contrast to my UCB approach. EI is typically more conservative (it only rewards improvement over the current best, not absolute predicted value), which might explain why your later-round queries clustered more tightly — EI naturally shifts toward exploitation as the best-observed value rises. UCB's κ parameter gives more direct control over the exploration-exploitation balance, but requires active tuning of κ rather than letting the acquisition function adapt automatically to the current best. Both have merit; the choice depends on how much manual intervention you want to retain.

Your repository's documentation — particularly the datasheet and model card — is thorough and well-structured.

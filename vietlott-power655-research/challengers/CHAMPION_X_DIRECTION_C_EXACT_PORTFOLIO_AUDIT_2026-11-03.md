# Champion-X Direction C — exact Power 6/55 six-ticket portfolio audit (2026-11-03)

## Objective and frozen constraints
User selected Direction C: optimize portfolio structure with exactly **six different tickets** and fixed cost, without claiming forecasts. Study **at least one 3/6, 4/6, 5/6, or 6/6 main-number hit**, number of simultaneous winning tickets, and exact probability under a fair uniform draw. Original Power R19 Frozen and Hybrid6 remain immutable; no learning from past winning results is used.

The exact reproducible executable is `power655_portfolio_exact_20261103.cpp`, compile with `g++ -std=c++17 -O3 power655_portfolio_exact_20261103.cpp -o exact && ./exact`. Exhaustively enumerate the **28,989,675 = C(55,6)** possible winning main-six sets and calculate the number of six-number matches on every ticket. No Monte Carlo and no dependence on lottery history. Independent C++ source is on the research branch, not the Frozen branch.

## Controlled portfolio designs
A: **36 disjoint labels**, exactly the preissued X0 tickets for draw #01419 (used solely as a fixed ticket template, **not scored against that draw**):
1. 02 04 07 19 21 26
2. 11 24 27 49 52 55
3. 05 18 28 36 41 47
4. 08 15 23 25 38 40
5. 01 06 13 14 34 51
6. 09 17 20 31 45 50

B: **33 unique labels**, three pairs of tickets each share one label: replace first entry in ticket 2 with 02, ticket 4 with 05, ticket 6 with 01; all six tickets distinct.

C: **30 unique labels**, the same three pairs of tickets share two labels: ticket 2 changes 11,24→02,04; ticket 4 changes 08,15→05,18; ticket 6 changes 09,17→01,06. All six tickets distinct.

D: **21 unique labels**, all six tickets share 02,04,07, replacing the first three positions in tickets 2..6 with these values; each six-number ticket remains distinct.

These are four **specific prespecified geometric designs**, not a proof of global optimization over all possible portfolios.

## Exact result counts / 28,989,675 possible draws

| Portfolio | Unique labels | any ticket >=3 | any >=4 | any >=5 | any =6 | at least 2 tickets >=3 | at least 2 tickets >=4 |
|---|---:|---:|---:|---:|---:|---:|---:|
| A disjoint36 | 36 | 2,312,490 | 107,610 | 1,770 | 6 | 6,000 | 0 |
| B overlap1 | 33 | 2,299,590 | 107,610 | 1,770 | 6 | 18,900 | 0 |
| C overlap2 | 30 | 2,249,430 | 107,502 | 1,770 | 6 | 69,060 | 108 |
| D shared_core3 | 21 | 1,802,840 | 101,265 | 1,770 | 6 | 360,020 | 5,805 |

Exact percentage probabilities:
| Portfolio | P(any >=3) | P(any >=4) | P(any >=5) | P(any =6) |
|---|---:|---:|---:|---:|
| A | 7.976944% | 0.371201% | 0.00610562% | 0.00002070% |
| B | 7.932445% | 0.371201% | 0.00610562% | 0.00002070% |
| C | 7.759418% | 0.370829% | 0.00610562% | 0.00002070% |
| D | 6.218904% | 0.349314% | 0.00610562% | 0.00002070% |

Full best-hit histogram (best=0..6):
- A: `[27132,10955088,15694965,2204880,105840,1764,6]`
- B: `[74613,11662557,14952915,2191980,105840,1764,6]`
- C: `[177100,12370596,14192549,2141928,105732,1764,6]`
- D: `[1344904,16067412,9774519,1701575,99495,1764,6]`

## Distinction between winning at least one ticket and concurrent wins
Across all four portfolios, **expected total number of winning tickets at each >=k threshold is identical** because each of six individual tickets has the same fair-draw distribution and expectation is linear:
- total outcomes×ticket counts with >=3 = 2,318,490
- >=4 = 107,610
- >=5 = 1,770
- =6 = 6.

But partial overlap makes wins more correlated: the **probability of at least one** winning ticket generally declines in these examples, while the chance of **two or more tickets** reaching a threshold can rise. For example, portfolio D achieves >=2 tickets with >=3 hits in 360,020 outcome combinations versus just 6,000 for A. This is a trade-off in payout variance / clustering, **not a proven EV improvement**. With fixed per-ticket prizes, same cost and six distinct tickets, expected gross payout is invariant under fair uniform draws (before jackpot pool sharing, promotions and payout variations). For progressive/parimutuel prizes, actual EV also depends on prize pool, ticket costs and sharing with other players—none was modeled here.

## Analytical implications
1. In the four tested designs, A maximizes probability of **at least one >=3 or >=4**; the more heavily overlapped portfolios sacrifice breadth and increase clustered outcomes. Do **not** overstate this as a global mathematical proof of optimality for every possible portfolio design.
2. No method changes six-ticket jackpot odds while every ticket remains unique: `6/C(55,6)=1/4,831,612.5` per draw, approximately 0.00002070%.
3. Changing how **36 disjoint numbers** are arranged into six tickets does not change their unconditional distribution of best-hit scores under independent uniform draws; all disjoint partitions are isomorphic under relabeling of numbers.
4. Increasing cross-ticket overlap changes the distribution of multiple prizes, not the fundamental per-ticket chance of any specified hit count.
5. The next honest decision is choosing a utility objective: maximize probability of any prize, or maximize probability of *multiple tickets* winning together, or optimize variance/utility conditional on a real payout table. There is no reason to claim historical prediction from these exact combinatorial results.

## Research state
Research branch only; original R19 Frozen, Hybrid6 and registered Champions untouched. This is an exhaustive combinatorial calculation, not a Python clean-checkout pass for the historical R19 replay, which remains separately unverified.

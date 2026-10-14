"""PREREG19 smoke test (disclosed): tiny tree, short sequences, every generator and the reader run end to end.
No registered cell is touched; nothing here is a statistic of the registration."""
import numpy as np
from sim_core import yule_tree, rescale_tree_depth, exact_patristic_matrix, evolve_jc69
from measures import hamming_matrix, jc_correct, sample_quartets, quartet_accuracy
from hgt_core import apply_hgt
from misspec_core import evolve_gamma, evolve_hky, evolve_heterotachy, hky_P

tree = rescale_tree_depth(yule_tree(32, seed=1), 1.0)
D = exact_patristic_matrix(tree); Q = sample_quartets(32, 300, seed=3)
P = hky_P(0.3, (0.15, 0.35, 0.35, 0.15), 4.0)
assert np.allclose(P.sum(1), 1) and P.min() >= 0, "HKY rows must be probabilities"
for name, seqs in [("jc", evolve_jc69(tree, 4000, 5)), ("gamma", evolve_gamma(tree, 4000, 5)),
                   ("hky", evolve_hky(tree, 4000, 5)), ("hetero", evolve_heterotachy(tree, 4000, 5)[0]),
                   ("hgt", apply_hgt(evolve_jc69(tree, 4000, 5), 0.3, 0.3, 9)[0])]:
    assert seqs.shape == (32, 4000) and seqs.dtype == np.int8
    d, sat = jc_correct(hamming_matrix(seqs))
    r = quartet_accuracy(D, d, Q, obs_valid_mask=~sat)
    comp = np.bincount(seqs.ravel(), minlength=4) / seqs.size
    print(f"{name:7s} acc_decided {r['accuracy_of_decided']:.3f} undecidable {r['fraction_undecidable']:.3f} composition {np.round(comp, 3).tolist()}")
print("SMOKE OK")

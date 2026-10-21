"""Synthetic unit fixtures verify mathematics and rejection gates, not real-video accuracy."""
import copy
import itertools
import unittest

import numpy as np

from fetch_results import parse_result
from order_tests import (eligible_draws,holm,mc_result,monte_carlo,position_expected,
    position_stat,remaining,special_stat,transition_expected,transition_stat,validate_draw)

def fixture():
    return [dict(draw_id='00001',draw_date='2000-01-01',source_id='fixture',source_sha256='fixture_hash',
        capture_index=str(i),ball_type='main' if i<7 else 'special',ball_number=str(i),
        readable_pts_start=str(i*10),readable_pts_end=str(i*10+1),
        primary_review='reviewer_a',secondary_review='reviewer_b',verification_status='verified_two_reviews') for i in range(1,8)]

class Phase3Tests(unittest.TestCase):
    def test_exact_enumeration_position_and_transition_expectation(self):
        permutations=np.asarray(list(itertools.permutations(range(1,7))))
        empirical_position=np.zeros((55,6));empirical_transition=np.zeros((55,55))
        for row in permutations:
            empirical_position[row-1,np.arange(6)]+=1/720
            empirical_transition[row[:-1]-1,row[1:]-1]+=1/720
        np.testing.assert_allclose(empirical_position,position_expected([[1,2,3,4,5,6]]),atol=1e-12)
        np.testing.assert_allclose(empirical_transition,transition_expected([[1,2,3,4,5,6]]),atol=1e-12)

    def test_single_draw_sparse_statistics_are_constant(self):
        e1=position_expected([[1,2,3,4,5,6]]);e2=transition_expected([[1,2,3,4,5,6]])
        for row in itertools.permutations(range(1,7)):
            self.assertAlmostEqual(position_stat([row],e1),30.)
            self.assertAlmostEqual(transition_stat([row],e2),25.)

    def test_remaining49_and_special_mechanism(self):
        rem=remaining([[1,2,3,4,5,6],[50,51,52,53,54,55]])
        self.assertEqual(rem.shape,(2,49));self.assertTrue(set(rem[0]).isdisjoint(range(1,7)))
        self.assertAlmostEqual(special_stat([31,25],rem),0.)
        with self.assertRaises(ValueError):monte_carlo([[1,2,3,4,5,6]],[6],b=9)

    def test_mc_add_one_and_interval_edge_cases(self):
        r=mc_result(2,[0,0,0]);self.assertEqual(r['p_value'],.25)
        self.assertEqual(r['mc_exceedance_ci_low'],0.)
        r=mc_result(0,[1,1,1]);self.assertEqual(r['p_value'],1.)
        self.assertEqual(r['mc_exceedance_ci_high'],1.)

    def test_holm_includes_fixed_family(self):
        r=holm({'H1':.01,'H2':.03,'H3':1.,'H4':1.,'SPECIAL':1.})
        self.assertAlmostEqual(r['H1'],.05);self.assertAlmostEqual(r['H2'],.12)

    def test_duplicate_capture_and_invalid_number_rejected(self):
        rows=fixture();validate_draw(rows)
        rows[1]['capture_index']='1'
        with self.assertRaises(ValueError):validate_draw(rows)
        rows=fixture();rows[1]['ball_number']='1'
        with self.assertRaises(ValueError):validate_draw(rows)
        rows=fixture();rows[0]['ball_number']='NA'
        with self.assertRaises(ValueError):validate_draw(rows)

    def test_invalid_role_pts_and_mixed_source_rejected(self):
        for key,value in [('ball_type','special'),('readable_pts_start','nan'),('source_id','different')]:
            rows=fixture();rows[0][key]=value
            with self.assertRaises(ValueError):validate_draw(rows)
        rows=fixture();rows[2]['readable_pts_end']='1'
        with self.assertRaises(ValueError):validate_draw(rows)
        rows=fixture();rows[2]['readable_pts_end']='nan'
        with self.assertRaises(ValueError):validate_draw(rows)

    def test_primary_excludes_provisional_and_same_reviewer(self):
        quality={'00001':{'official_result_status':'verified'}}
        good=fixture();self.assertEqual(len(eligible_draws(good,quality)[0]),1)
        for mutation in ('provisional','same','missing'):
            rows=copy.deepcopy(good)
            for r in rows:
                if mutation=='provisional':r['verification_status']='provisional_one_review'
                elif mutation=='same':r['secondary_review']=r['primary_review']
                else:r['secondary_review']='NA'
            self.assertEqual(eligible_draws(rows,quality)[0],[])

    def test_official_403_or_secondary_result_cannot_qualify(self):
        for status in ('unavailable_http_403','secondary_matched','not_verified'):
            self.assertEqual(eligible_draws(fixture(),{'00001':{'official_result_status':status}})[0],[])

    def test_deterministic_draw_cluster_permutation(self):
        main=[[1,4,9,12,21,38],[3,4,21,39,47,55]];special=[55,1]
        a=monte_carlo(main,special,b=199,seed=7);b=monte_carlo(main,special,b=199,seed=7)
        self.assertEqual(a,b)
        for v in a.values():self.assertGreater(v['p_value'],0);self.assertLessEqual(v['p_value'],1)
        np.testing.assert_array_equal(main,[[1,4,9,12,21,38],[3,4,21,39,47,55]])

    def test_published_result_parser_never_uses_sorted_order_as_labels(self):
        html='Kỳ vé: <span>#00001</span> '+''.join(f'<li><div class="finnish1 bool">{n:02d}</div></li>' for n in range(1,8))+'</ul>'
        self.assertEqual(parse_result(html,'00001')[0],list(range(1,8)))
        self.assertEqual(parse_result(html,'99999')[0],[])

if __name__=='__main__':unittest.main()

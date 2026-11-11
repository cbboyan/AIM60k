% AIM60k problem L1dist_to_aa1__goal_58: goal 58 of original L1dist_to_aa1, proof line 379.
% Axiom names and symbols: see axioms.ax.

cnf(left_id,axiom,m(e,A) = A).
cnf(right_id,axiom,m(A,e) = A).
cnf(ld_cancel,axiom,ld(A,m(A,B)) = B).
cnf(ld_mult,axiom,m(A,ld(A,B)) = B).
cnf(rd_cancel,axiom,rd(m(A,B),B) = A).
cnf(rd_mult,axiom,m(rd(A,B),B) = A).
cnf(def_a,axiom,a(A,B,C) = ld(m(A,m(B,C)),m(m(A,B),C))).
cnf(def_k,axiom,k(A,B) = ld(m(B,A),m(A,B))).
cnf(def_l,axiom,l(A,B,C) = ld(m(C,B),m(C,m(B,A)))).
cnf(def_r,axiom,r(A,B,C) = rd(m(m(A,B),C),m(B,C))).
cnf(def_t,axiom,t(A,B) = ld(B,m(A,B))).
cnf(aim_tt,axiom,t(t(A,B),C) = t(t(A,C),B)).
cnf(aim_tl,axiom,l(t(A,B),C,D) = t(l(A,C,D),B)).
cnf(aim_tr,axiom,r(t(A,B),C,D) = t(r(A,C,D),B)).
cnf(aim_lr,axiom,r(l(A,B,C),D,E) = l(r(A,D,E),B,C)).
cnf(aim_ll,axiom,l(l(A,B,C),D,E) = l(l(A,D,E),B,C)).
cnf(aim_rr,axiom,r(r(A,B,C),D,E) = r(r(A,D,E),B,C)).
cnf(l1dist,axiom,m(l(A,B,C),l(D,B,C)) = l(m(A,D),B,C)).
fof(goal_58_line_379,conjecture,! [X0,X1] : X0 = r(t(rd(X1,rd(X1,X0)),X1),rd(X1,X0),X0)).

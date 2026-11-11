% AIM60k problem raa2a__goal_122: goal 122 of original raa2a, proof line 1182.
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
cnf(aa1,axiom,a(a(A,B,C),D,E) = e).
cnf(nucsq_r,axiom,m(m(A,B),m(C,C)) = m(A,m(B,m(C,C)))).
fof(goal_122_line_1182,conjecture,! [X0,X1,X2] : m(m(X0,X1),m(k(X1,X0),t(ld(k(X1,X0),e),X2))) = m(m(X1,X0),t(k(X0,X1),X2))).

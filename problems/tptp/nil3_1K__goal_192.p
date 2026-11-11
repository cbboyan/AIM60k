% AIM60k problem nil3_1K__goal_192: goal 192 of original nil3_1K, proof line 790.
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
cnf(nil3_1,axiom,k(A,k(B,k(C,D))) = e).
cnf(nil3_2,axiom,k(k(A,a(B,C,D)),E) = e).
cnf(nil3_3,axiom,k(a(k(A,B),C,D),E) = e).
cnf(nil3_4,axiom,k(a(A,k(B,C),D),E) = e).
cnf(nil3_5,axiom,k(a(A,B,k(C,D)),E) = e).
cnf(nil3_9,axiom,a(k(A,k(B,C)),D,E) = e).
cnf(nil3_10,axiom,a(A,k(B,k(C,D)),E) = e).
cnf(nil3_11,axiom,a(A,B,k(C,k(D,E))) = e).
cnf(nil3_23,axiom,a(A,B,a(C,D,k(E,F))) = e).
fof(goal_192_line_790,conjecture,! [X0,X1] : m(X0,m(ld(ld(X0,e),X1),ld(X0,e))) = t(m(X0,X1),ld(X0,e))).

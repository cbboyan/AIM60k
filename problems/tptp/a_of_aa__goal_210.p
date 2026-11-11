% axioms: BASE AA_NL AA_NM nil3_15
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
cnf(nil3_15,axiom,a(a(k(A,B),C,D),E,F) = e).
cnf(nil3_24,axiom,a(a(a(A,B,C),D,E),F,V6) = e).
cnf(nil3_25,axiom,a(a(A,a(B,C,D),E),F,V6) = e).
cnf(nil3_26,axiom,a(a(A,B,a(C,D,E)),F,V6) = e).
cnf(nil3_27,axiom,a(A,a(a(B,C,D),E,F),V6) = e).
cnf(nil3_28,axiom,a(A,a(B,a(C,D,E),F),V6) = e).
cnf(nil3_29,axiom,a(A,a(B,C,a(D,E,F)),V6) = e).
fof(goal_210_line_1375,conjecture,! [X0,X1,X2,X3] : (X0 != m(k(X1,X2),k(X3,X1)) | X0 = m(k(X3,X1),k(X1,X2)))).

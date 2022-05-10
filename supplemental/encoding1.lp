:- concl,nconcl.					% consistency
concl :- prem(X), sufficient(X).	% conditional with sufficient condition
nconcl :- nprem(X), necessary(X).	% conditional with necessary condition
{prem(X); nprem(X)}1 :- hyp(X).		% hypothesis
nconcl :- nprem(e), nprem(t).		% conditional with all sufficient conditions

sufficient(e).
sufficient(t).
necessary(o).
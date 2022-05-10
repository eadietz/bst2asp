necessary(e).
{hyp(o);hyp(e)}1. % minimal explanation

% Abduction, ask whether there is a way to set nprem(e) to true.
% First we ask for (P \cup O) = (P \cup {:- not nconcl})
:- not nconcl.
% Secondly we ask for (P \cup O \cup E) = (P \cup {:- not nconcl} \cup {:- not nprem(e)})
query(nprem(e)).

hyp(e). 
{necessary(e)}.

{concl}.

% Abduction, ask whether there is a way to set prem(e) to true. 
% First we ask for (P \cup O) = (P \cup {:- not concl})
:- not concl.

% Secondly we ask for (P \cup O \cup E) = (P \cup {:- not concl} \cup {:- not prem(e)})
query(prem(e)).
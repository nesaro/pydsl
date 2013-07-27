declaration = r'''# note use of raw string when embedding in python code...
file           :=  [ \t\n]*, section+
section        :=  '[',identifier!,']'!, ts,'\n', body
body           :=  statement*
statement      :=  (ts,semicolon_comment)/equality/nullline
nullline       :=  ts,'\n'
comment        :=  -'\n'*
equality       :=  ts, identifier,ts,'=',ts,identified,ts,'\n'
identifier     :=  [a-zA-Z], [a-zA-Z0-9_]*
identified     :=  string/number/identifier
ts             :=  [ \t]*
'''


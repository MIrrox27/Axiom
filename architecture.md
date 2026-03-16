<div align="center">
<h1>Project architecture</h1>
</div>

```
axiom-lang/
│
├── axiom/                      
│   ├── __init__.py
│   ├── __main__.py              
│   ├── lexer.py                 
│   ├── parser.py                
│   ├── ast_nodes.py             
│   ├── tokens.py               
│   ├── interpreter.py           
│   └── repl.py                  
│
├── doc/
│    ├── 01-getting-started.md      
│    ├── 02-syntax.md                
│    ├── 03-variables.md (var, val)
│    ├── 04-operators.md 
│    ├── 05-control-flow.md (if, while, for, foreach, do)
│    ├── 06-builtins.md (print, input)
│    ├── 07-examples.md            
│    └──  08-api.md                                    
│
├── examples/                    
│   ├── hello.ax
│   ├── fibonacci.ax
│   └── 
│
├── tests/                       
│   └── test_interpreter.py
│
├── setup.py                     
└── README.md
```                   



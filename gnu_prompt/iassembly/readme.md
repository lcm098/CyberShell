

eTypeRegisters

    eax
    ebx
    ecx
    edx
    eex
    efx
    egx
    ehx
    eix
    ejx
    ekx
    elx
    emx
    enx
    eox
    epx
    eqx
    erx
    esx
    etx
    eux
    evx
    ewx
    exx
    eyx
    ezx


fTypeRegister
    fptr

rTypeRegister
    rptr

cTypeRegister
    cptr

vTypeRegister
    vptr


ObjectTypeRegisters
    identifier  --> could be any identifier (this not comes in any register category)
    persistent  --> pas, pbs, pcs, pds, pes, pfs, pxs, pzs
    const   --> ras, rbs, rcs, rds, res, rfs, rxs, rzx



* RULE 1
    any function take a list as function arguments


* RULE 2
    fTypeRegister only used as passing function's arguments, and i have to link before function call

* RULE 3
    rTypeRegister only used as return function's final value, which is very useful
    for nested function call, for StanderLibrary rptr will automatic defines or assign again when function return any value in the form of list


* RULE 4
    vTypeRegister only used to store computed numeric operation's value

* RULE 5
    cTypeRegister only used to store compared value in cmp, elif, else
    if elif block runs then the value of cptr will be set to True, and same happend with cmp, but if condition falls in else then it set value of cptr to False

* RULE 6
    to load (v, c, f, r)Register to eTypeRegister we use 'load' opcode (operation code)

* RULE 7
    to link eTypeRegister to (v, c, f, r)Register we use 'link' opcode (operation code)

* RULE 8
    to link (identifier), (persistent) and (const) to eTypeRegister we write mov OpCode

* RULE 9
    while access list, dict items we write #list_name[index] or #dict_name[element], '#' is very necessary to write

* RULE 10
    every statement can not exceed more than one OpCode and two opponents, x, y

* RULE 11
    maximum statement Operations range can be three like (mov eax, 10)

* RULE 12
    minimum statement Operation range can be 1 like (pusha, popa)



Now Take Over From Ground, and start learning The INTERNATIONAL ASSEMBLY (by Danishk sinha, creator of this language)


Purpose









chapters

1. HelloWorld
2. syntax
3. condition
4. loops
5. jump and label
6. enum
7. struct
8.
9.
10.
11.
12.
13
14.


1. HelloWorld
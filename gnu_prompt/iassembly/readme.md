""" A very simple code to print Hello World in IC_Assembly """
""" in IC Assembly, we use Very Special Variables at the place of Registers """

section .text ||

    mov ras, "Hello"  // move "Hello" string to ras (vs variable)
    load fptr, @[ras] // load vs-var as (array group) to function pointer
    call write, rdo_var        // call write function to print it
    unload fptr       // nice way to unload fptr, every time after load


    

    link arr, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    load fptr, @[arr]
    call write, rdo_var
    unload fptr

    link dict, {"ram":1, "shyam":2, "mohan":3}
    load fptr, @[dict]
    call write, rdo_var
    unload fptr

    link list, ["anoop", 1, false, nil]
    load fptr, @[list]
    call write, rdo_var
    unload fptr

    load fptr, @[age, gender] 
    call read, rdo_var                //call stander read for input  

    // introduction ecx (which is result resolver variable)

    mov ecx_res, fptr   // move fptr value to ecx_res variable
    unload fptr         // unload the previous persistence of read function

    cmp [(age >= 21) & (gender == 'm')]
    if rdo_var, true
    [
        link name
        load fptr, @["Hello ", name, " You Can Drive!"]
        call write, rdo_var
        unload fptr
    ]
    if rdo_var, false
    [
        load fptr, @["Hello ", name, " You Can Not Drive"]
        call write, rdo_var
        unload fptr
    ]

    mov ras, 3
    mov rbs, 4
    load fptr, @[ras, rbs]
    call add_num
    mov rcs, vptr  // 7 value will store in rcs special variable


    add_num [
        pusha    // create persistence
        add ras, rbs
        mov rcs, rdo_var
        mov vptr, rcs
        popa

        return vptr
    ]

    // struct uses
    invoke my_data, arr
    mov dsptr, rdo_var
    set dsptr, 55
    inc dsptr

    set dsptr, 77
    inc dsptr

    set dsptr, 99
    inc dsptr
    inject my_data, arr

    invoke my_data, arr
    mov dsptr, rdo_var
    get dsptr
    mov ras, rdo_var
    inc dsptr

    get dsptr
    mov ras, rdo_var
    inc dsptr

    get dsptr
    mov ras, rdo_var
    inc dsptr
    inject my_data, arr
    
    // .data uses
    link fs
    mov ras, fs[1] // get
    mov fs[1], 55 // set
||

// in .struct we can only declare
section .struct my_data {
    da arr 3
}

// in .data we can declare and initialize both
section .data ||
    
    da arr 10
    dd dict 3
    dl list 4
    
    dr name "danishk"
    dr age 3
    dr gender 1

    da fs [1, 2, 3, 4]
||
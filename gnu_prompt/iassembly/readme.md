""" A very simple code to print Hello World in IC_Assembly """
""" in IC Assembly, we use Very Special Variables at the place of Registers """

section .text ||

    mov ras, "Hello"  // move "Hello" string to ras (vs variable)
    load fptr, %[#ras] // load ras-var as (array group) to function pointer var
    call write, fptr        // call write function to print it
    unload fptr       // nice way to unload fptr, every time after load


    cmp [(age >= 21) & (gender == 'm')]
    if rdo_var, true
    [
        
    ]
    if rdo_var, false
    [
        
    ]


    //function
    add_num [
        
    ]

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
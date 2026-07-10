module Adder_top();

  logic [63:0] a;
  logic [63:0] b;
  logic  cin;
  logic [62:0] sum;
  logic  cout;


 Adder Adder(
    .a(a),
    .b(b),
    .cin(cin),
    .sum(sum),
    .cout(cout)
 );


  export "DPI-C" function get_axxPfBDHOuJFOQ;
  export "DPI-C" function set_axxPfBDHOuJFOQ;
  export "DPI-C" function get_bxxPfBDHOuJFOQ;
  export "DPI-C" function set_bxxPfBDHOuJFOQ;
  export "DPI-C" function get_cinxxPfBDHOuJFOQ;
  export "DPI-C" function set_cinxxPfBDHOuJFOQ;
  export "DPI-C" function get_sumxxPfBDHOuJFOQ;
  export "DPI-C" function get_coutxxPfBDHOuJFOQ;


  function void get_axxPfBDHOuJFOQ;
    output logic [63:0] value;
    value=a;
  endfunction

  function void set_axxPfBDHOuJFOQ;
    input logic [63:0] value;
    a=value;
  endfunction

  function void get_bxxPfBDHOuJFOQ;
    output logic [63:0] value;
    value=b;
  endfunction

  function void set_bxxPfBDHOuJFOQ;
    input logic [63:0] value;
    b=value;
  endfunction

  function void get_cinxxPfBDHOuJFOQ;
    output logic  value;
    value=cin;
  endfunction

  function void set_cinxxPfBDHOuJFOQ;
    input logic  value;
    cin=value;
  endfunction

  function void get_sumxxPfBDHOuJFOQ;
    output logic [62:0] value;
    value=sum;
  endfunction

  function void get_coutxxPfBDHOuJFOQ;
    output logic  value;
    value=cout;
  endfunction



  initial begin
    $dumpfile("./output/Adder/Adder.fst");
    $dumpvars(0, Adder_top);
  end

  export "DPI-C" function finish_PfBDHOuJFOQ;
  function void finish_PfBDHOuJFOQ;
    $finish;
  endfunction


endmodule

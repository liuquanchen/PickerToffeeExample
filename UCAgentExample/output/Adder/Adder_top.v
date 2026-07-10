module Adder_top;

  wire [63:0] a;
  wire [63:0] b;
  wire  cin;
  wire [62:0] sum;
  wire  cout;


 Adder Adder(
    .a(a),
    .b(b),
    .cin(cin),
    .sum(sum),
    .cout(cout)
 );


endmodule

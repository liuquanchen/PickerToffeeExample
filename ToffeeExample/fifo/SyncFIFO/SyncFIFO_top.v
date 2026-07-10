module SyncFIFO_top;

  wire  clk;
  wire  rst_n;
  wire  we_i;
  wire  re_i;
  wire [31:0] data_i;
  wire [31:0] data_o;
  wire  full_o;
  wire  empty_o;


 SyncFIFO SyncFIFO(
    .clk(clk),
    .rst_n(rst_n),
    .we_i(we_i),
    .re_i(re_i),
    .data_i(data_i),
    .data_o(data_o),
    .full_o(full_o),
    .empty_o(empty_o)
 );


endmodule

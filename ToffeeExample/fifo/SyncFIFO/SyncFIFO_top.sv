module SyncFIFO_top();

  logic  clk;
  logic  rst_n;
  logic  we_i;
  logic  re_i;
  logic [31:0] data_i;
  logic [31:0] data_o;
  logic  full_o;
  logic  empty_o;


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


  export "DPI-C" function get_clkxxGZjt4pl0o6W;
  export "DPI-C" function set_clkxxGZjt4pl0o6W;
  export "DPI-C" function get_rst_nxxGZjt4pl0o6W;
  export "DPI-C" function set_rst_nxxGZjt4pl0o6W;
  export "DPI-C" function get_we_ixxGZjt4pl0o6W;
  export "DPI-C" function set_we_ixxGZjt4pl0o6W;
  export "DPI-C" function get_re_ixxGZjt4pl0o6W;
  export "DPI-C" function set_re_ixxGZjt4pl0o6W;
  export "DPI-C" function get_data_ixxGZjt4pl0o6W;
  export "DPI-C" function set_data_ixxGZjt4pl0o6W;
  export "DPI-C" function get_data_oxxGZjt4pl0o6W;
  export "DPI-C" function get_full_oxxGZjt4pl0o6W;
  export "DPI-C" function get_empty_oxxGZjt4pl0o6W;


  function void get_clkxxGZjt4pl0o6W;
    output logic  value;
    value=clk;
  endfunction

  function void set_clkxxGZjt4pl0o6W;
    input logic  value;
    clk=value;
  endfunction

  function void get_rst_nxxGZjt4pl0o6W;
    output logic  value;
    value=rst_n;
  endfunction

  function void set_rst_nxxGZjt4pl0o6W;
    input logic  value;
    rst_n=value;
  endfunction

  function void get_we_ixxGZjt4pl0o6W;
    output logic  value;
    value=we_i;
  endfunction

  function void set_we_ixxGZjt4pl0o6W;
    input logic  value;
    we_i=value;
  endfunction

  function void get_re_ixxGZjt4pl0o6W;
    output logic  value;
    value=re_i;
  endfunction

  function void set_re_ixxGZjt4pl0o6W;
    input logic  value;
    re_i=value;
  endfunction

  function void get_data_ixxGZjt4pl0o6W;
    output logic [31:0] value;
    value=data_i;
  endfunction

  function void set_data_ixxGZjt4pl0o6W;
    input logic [31:0] value;
    data_i=value;
  endfunction

  function void get_data_oxxGZjt4pl0o6W;
    output logic [31:0] value;
    value=data_o;
  endfunction

  function void get_full_oxxGZjt4pl0o6W;
    output logic  value;
    value=full_o;
  endfunction

  function void get_empty_oxxGZjt4pl0o6W;
    output logic  value;
    value=empty_o;
  endfunction



  initial begin
    $dumpfile("SyncFIFO.fst");
    $dumpvars(0, SyncFIFO_top);
  end

  export "DPI-C" function finish_GZjt4pl0o6W;
  function void finish_GZjt4pl0o6W;
    $finish;
  endfunction


endmodule

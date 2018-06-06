module simple_divider(quotient,dividend,divider,start,clk,bit);

   input [9:0]  dividend,divider;
   input         start, clk;
   output [9:0] quotient;
   output        bit;


   reg [9:0]    quotient;
   reg [19:0]    dividend_copy, divider_copy, diff;

   wire         bit;

   initial bit = 0;

   always @( posedge clk )

     if ( !(bit > 0) && start ) begin

        bit = 10;
        quotient = 0;
        dividend_copy = {10'd0,dividend};
        divider_copy = {1'b0,divider,9'd0};

     end else if ( bit > 0) begin

        diff = dividend_copy - divider_copy;

        if (diff > 0) begin
          quotient = { quotient[8:0], 1'b1 };
        end
        
        else begin
          quotient = { quotient[8:0], 1'b0 };
        end

        divider_copy = { 1'b0, divider_copy[19:1] };
        bit = bit - 1;

     end

endmodule

module Validator(
	input [9:0]in,
	input [9:0]avg_l,
	output flag
	);

wire [9:0]avg_u;
wire [9:0]upper, [9:0]lower;

avg_u = avg_l + 1;
upper = avg_u * avg_u;
lower = avg_l * avg_l;

flag = (upper > in) && (lower <= in);

endmodule

module Sqrt(
	input clk,
	input rst,
	input [9:0]in,
	output [9:0]out
	);

reg  [9:0]guess;
wire [9:0]avg;
reg  [9:0]sum;
wire [9:0]quot;

wire clk_div, flag_found;

always @(posedge clk_div or posedge rst) begin
	if (rst)
	begin
		guess <= in >> 1;
	end
	else
	begin
		guess <= avg; 
	end
end

Divider D1(
	.clk(clk),
	.start(!flag_found),
	.dividend(in),
	.diviser(guess),
	.quotient(quot),
	.bit(clk_div)
	);

always @(posedge clk_div or posedge rst) begin
	if (rst)
	begin
		sum <= 10'd0;
	end
	else
	begin
		sum <= guess + quot;
	end
end

avg = sum >> 1;

Validator V1(
	.in(in),
	.avg(avg),
	.flag(flag_found)
	);

always @*
begin
	if(flag_found)
	begin
		out = avg;
	end
	else
	begin
		out = 10'd0;
	end
end

endmodule
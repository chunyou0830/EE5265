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
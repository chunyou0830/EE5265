module HalfAdder(
	output s,
	output co,
	input a,
	input b
	);

assign s = a^b;
assign co = a&b;

endmodule
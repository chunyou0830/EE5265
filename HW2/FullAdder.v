module FullAdder(
	output co,
	output s,
	input a,
	input b,
	input ci
	);

wire t0,t1,t2;

HalfAdder H0(.s(t0),.co(t1),.a(a),.b(b));
HalfAdder H1(.s(s),.co(t2),.a(t0),.b(ci));

assign co = t1|t2;

endmodule
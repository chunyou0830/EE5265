module TenBitAdder(
	input [9:0]a,
	input [9:0]b,
	input ci,
	output [9:0]s,
	output co
	);

wire c1,c2,c3,c4,c5,c6,c7,c8,c9;

FullAdder F0(.co(c1),.s(s[0]),.a(a[0]),.b(b[0]),.ci(ci));
FullAdder F1(.co(c2),.s(s[1]),.a(a[1]),.b(b[1]),.ci(c1));
FullAdder F2(.co(c3),.s(s[2]),.a(a[2]),.b(b[2]),.ci(c2));
FullAdder F3(.co(c4),.s(s[3]),.a(a[3]),.b(b[3]),.ci(c3));
FullAdder F4(.co(c5),.s(s[4]),.a(a[4]),.b(b[4]),.ci(c4));
FullAdder F5(.co(c6),.s(s[5]),.a(a[5]),.b(b[5]),.ci(c5));
FullAdder F6(.co(c7),.s(s[6]),.a(a[6]),.b(b[6]),.ci(c6));
FullAdder F7(.co(c8),.s(s[7]),.a(a[7]),.b(b[7]),.ci(c7));
FullAdder F8(.co(c9),.s(s[8]),.a(a[8]),.b(b[8]),.ci(c8));
FullAdder F9(.co(co),.s(s[9]),.a(a[9]),.b(b[9]),.ci(c9));

endmodule
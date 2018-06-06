#include <iostream>
#include <cmath>

using namespace std;

int main(void){
	int x;
	cin >> x;

	int g = x / 2;
	int avg;

	cout << endl;

	for(int i = 0; i < 20; i++){
		avg = (g + x/g) / 2;
		g = avg;
		cout << "g= " << g << "\t g*g= " << g*g << "\t equal_flag= " << (abs(g*g - x)<0.000001) << endl;
	}

	cout << endl;

	cout << "Calc by self imp: " << avg << endl;

	cout << "Calc by math lib: " << sqrt(x) << endl;
}
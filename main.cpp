#include <iostream>
#include "Calculator.h"

using namespace std;

int main() {
    cout << "Calculator Starting" << endl << endl;

    Calculator calculator;

    Operator op1(3);
    Number n1(2.5);
    Number n2(3.8);

    calculator.insertOperator(&n1);
    calculator.insertOperator(&op1);
    calculator.insertOperator(&n2);
    calculator.print();

    return 0;
}

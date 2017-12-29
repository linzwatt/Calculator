#include "Calculator.h"
#include <typeinfo>

Calculator::Calculator() {
    this->calc[0] = new Operator(0);
}

Calculator::~Calculator() {
    //dtor
}

void Calculator::solve() {

}

void Calculator::print() {
    for (int i=0; i<this->nextIndex; ++i) {
        std::cout << *this->calc[i] << ' ';
    }
}

int Calculator::insertOperator(Operator* newOp) {
    if (this->nextIndex >= CALC_BUFFER) {
        this->nextIndex = CALC_BUFFER;
        return false;
    }

    this->calc[this->nextIndex] = newOp;
    ++this->nextIndex;
    return true;
}

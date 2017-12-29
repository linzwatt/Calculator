#include "Operator.h"

Operator::Operator(int type) {
    this->type = type;
}

Operator::~Operator() {
    //dtor
}

void Operator::print(std::ostream& os) const {
    os << symbols[this->type];
}

#include "Number.h"

Number::Number(double value) : Operator(-1) {
    this->value = value;
}

Number::~Number() {
    //dtor
}

void Number::print(std::ostream& os) const {
    os << this->value;
}

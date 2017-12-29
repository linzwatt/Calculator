#ifndef CALCULATOR_H
#define CALCULATOR_H

#include "Operator.h"
#include "Number.h"

#define CALC_BUFFER 100

class Calculator {
    public:
        Calculator();
        virtual ~Calculator();

        // FUNCTIONS
        int insertOperator(Operator* newOp);
        void solve();
        void print();

        // VARIABLES
        Operator* calc[CALC_BUFFER];
        int nextIndex = 0;

    protected:

    private:

};



#endif // CALCULATOR_H

#ifndef OPERATOR_H
#define OPERATOR_H

#include <iostream>

class Operator {
    public:
        Operator(int type);
        virtual ~Operator();

        // FUNCTIONS
        virtual void print(std::ostream&) const;
        friend std::ostream& operator<<(std::ostream& os, const Operator& op) {
            op.print(os);
            return os;
        }

        // VARIABLES
        int type;

        // CONSTANTS
        char symbols[7] = {'+', '-', '*', '/', '^', '(', ')'};

    protected:

    private:
};

#endif // OPERATOR_H

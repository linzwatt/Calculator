#ifndef NUMBER_H
#define NUMBER_H

#include <Operator.h>


class Number : public Operator
{
    public:
        Number(double value);
        virtual ~Number();
        virtual void print(std::ostream&) const;

        double value;

    protected:

    private:
};

#endif // NUMBER_H

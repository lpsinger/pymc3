import theano.tensor as tt

__all__ = ['Zero', 'Constant', 'Linear']


class Mean(object):
    R"""
    Base class for mean functions
    """

    def __call__(self, X):
        R"""
        Evaluate the mean function.

        Parameters
        ----------
        X : The training inputs to the mean function.
        """
        raise NotImplementedError

    def __add__(self, other):
        return Add(self, other)

    def __mul__(self, other):
        return Prod(self, other)


class Zero(Mean):
    R"""
    Zero mean function for Gaussian process.

    """

    def __call__(self, X):
        return tt.alloc(0.0, X.shape[0])

class Constant(Mean):
    R"""
    Constant mean function for Gaussian process.

    Parameters
    ----------
    c : variable, array or integer
        Constant mean value
    """

    def __init__(self, c=0):
        Mean.__init__(self)
        self.c = c

    def __call__(self, X):
        return tt.alloc(1.0, X.shape[0]) * self.c


class Linear(Mean):
    R"""
    Linear mean function for Gaussian process.

    Parameters
    ----------
    coeffs : variables
        Linear coefficients
    intercept : variable, array or integer
        Intercept for linear function (Defaults to zero)
    """

    def __init__(self, coeffs, intercept=0):
        Mean.__init__(self)
        self.b = intercept
        self.A = coeffs

    def __call__(self, X):
        return tt.squeeze(tt.dot(X, self.A) + self.b)


class Add(Mean):
    def __init__(self, first_mean, second_mean):
        Mean.__init__(self)
        self.m1 = first_mean
        self.m2 = second_mean

    def __call__(self, X):
        return tt.add(self.m1(X), self.m2(X))


class Prod(Mean):
    def __init__(self, first_mean, second_mean):
        Mean.__init__(self)
        self.m1 = first_mean
        self.m2 = second_mean

    def __call__(self, X):
        return tt.mul(self.m1(X), self.m2(X))


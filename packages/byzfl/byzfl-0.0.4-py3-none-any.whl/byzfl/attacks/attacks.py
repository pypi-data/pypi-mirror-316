import numpy as np
from byzfl.utils.misc import check_vectors_type

class NoAttack(object):

    """
    Description
    -----------
    Class representing an attack which behaves like an honest node.

    Methods
    ---------
    """
    def __init__(self):
        pass 
    
    def __call__(self, honest_vectors):
        """
        Compute the arithmetic mean along axis = 0.
        Returns the average of the array elements.

        Parameters
        ----------
        honest_vectors : 2D ndarray or 2D torch.tensor with floating point or complex dtype
            Matrix containing arrays whose mean is desired.

        Returns
        -------
        mean_vector : ndarray or torch.tensor
            The mean vector of the input. The dtype of the outputs is the same as the input.

        Examples
        --------
        With numpy arrays:
            >>> matrix = np.array([[1., 2., 3.], 
            >>>                    [4., 5., 6.], 
            >>>                    [7., 8., 9.]])
            >>> attack = NoAttack()
            >>> result = attack.get_malicious_vector(matrix)
            >>> print(result)
            ndarray([4. 5. 6.])
        With torch tensors (Warning: We need the tensor to be either a floating point or complex dtype):
            >>> matrix = torch.stack([torch.tensor([1., 2., 3.]),
            >>>                       torch.tensor([4., 5., 6.]), 
            >>>                       torch.tensor([7., 8., 9.])])
            >>> attack = NoAttack()
            >>> result = attack.get_malicious_vector(matrix)
            >>> print(result)
            tensor([4., 5., 6.])
        """

        tools, honest_vectors = check_vectors_type(honest_vectors)
        mean_vector = tools.mean(honest_vectors, axis=0)
        return mean_vector


class SignFlipping:
    
    r"""
    
    Execute the Sign Flipping attack [1]_: send the opposite of the mean vector.

    .. math::

        \mathrm{SignFlipping} \ (x_1, \dots, x_n) = - \frac{1}{n}\sum_{i=1}^{n} x_i

    where

    - :math:`x_1, \dots, x_n` are the input vectors, which conceptually correspond to correct gradients submitted by honest participants during a training iteration.
    
    Initialization parameters
    --------------------------

    None

    Calling the instance
    --------------------

    Input parameters
    ----------------

    vectors: numpy.ndarray, torch.Tensor, list of numpy.ndarray or list of torch.Tensor
        A set of vectors, matrix or tensors.

    Returns
    -------
    :numpy.ndarray or torch.Tensor
        The data type of the output is the same as the input.

    Examples
    --------

        >>> import byzfl
        >>> attack = byzfl.SignFlipping()

        Using numpy arrays
            
        >>> import numpy as np
        >>> x = np.array([[1., 2., 3.],       # np.ndarray
        >>>               [4., 5., 6.], 
        >>>               [7., 8., 9.]])
        >>> attack(x)
        array([-4. -5. -6.])
                
        Using torch tensors
            
        >>> import torch
        >>> x = torch.tensor([[1., 2., 3.],   # torch.tensor 
        >>>                   [4., 5., 6.], 
        >>>                   [7., 8., 9.]])
        >>> attack(x)
        tensor([-4., -5., -6.])

        Using list of numpy arrays

        >>> import numppy as np
        >>> x = [np.array([1., 2., 3.]),      # list of np.ndarray  
        >>>      np.array([4., 5., 6.]), 
        >>>      np.array([7., 8., 9.])]
        >>> attack(x)
        array([-4., -5., -6.])

        Using list of torch tensors
            
        >>> import torch
        >>> x = [torch.tensor([1., 2., 3.]),  # list of torch.tensor 
        >>>      torch.tensor([4., 5., 6.]), 
        >>>      torch.tensor([7., 8., 9.])]
        >>> attack(x)
        tensor([-4., -5., -6.])


    References
    ----------

    .. [1] Zeyuan Allen-Zhu, Faeze Ebrahimianghazani, Jerry Li, and Dan Alistarh. Byzantine-resilient non-convex stochastic gradient descent.
        In International Conference on Learning Representations, 2020

    """

    def __init__(self):
        pass
    
    def __call__(self, honest_vectors):
        tools, honest_vectors = check_vectors_type(honest_vectors)
        mean_vector = tools.mean(honest_vectors, axis=0)
        return tools.multiply(mean_vector, -1)


class FallOfEmpires:
    
    r"""
    Description
    -----------

    Execute the Fall of Empires (FoE) attack [1]_: multiplicatively scale the mean vector by :math:`1 - \tau`.

    .. math::

        \text{FoE}_{\tau}(x_1, \dots, x_n) = 
        (1 - \tau) \cdot \frac{1}{n} \sum_{i=1}^{n} x_i

    where 

    - :math:`x_1, \dots, x_n` are the input vectors, which conceptually correspond to correct gradients submitted by honest participants during a training iteration.

    -  :math:`\tau` is the attack factor.

    Initialization parameters
    --------------------------

    tau : int or float
        The attack factor :math:`\tau` used to adjust the mean vector. Set to 3 by default.

    Calling the instance
    --------------------

    Input parameters
    ----------------

    vectors: numpy.ndarray, torch.Tensor, list of numpy.ndarray or list of torch.Tensor
        A set of vectors, matrix or tensors.
    

    Returns
    -------
    :numpy.ndarray or torch.Tensor
        The data type of the output is the same as the input.
    
    Examples
    --------

    >>> import byzfl
    >>> attack = byzfl.FallOfEmpires(3)

    Using numpy arrays
        
    >>> import numpy as np
    >>> x = np.array([[1., 2., 3.],       # np.ndarray
    >>>               [4., 5., 6.], 
    >>>               [7., 8., 9.]])
    >>> attack(x)
    array([ -8. -10. -12.])
            
    Using torch tensors
        
    >>> import torch
    >>> x = torch.tensor([[1., 2., 3.],   # torch.tensor 
    >>>                   [4., 5., 6.], 
    >>>                   [7., 8., 9.]])
    >>> attack(x)
    tensor([-8., -10., -12.])

    Using list of numpy arrays

    >>> import numppy as np
    >>> x = [np.array([1., 2., 3.]),      # list of np.ndarray  
    >>>      np.array([4., 5., 6.]), 
    >>>      np.array([7., 8., 9.])]
    >>> attack(x)
    array([ -8. -10. -12.])

    Using list of torch tensors
        
    >>> import torch
    >>> x = [torch.tensor([1., 2., 3.]),  # list of torch.tensor 
    >>>      torch.tensor([4., 5., 6.]), 
    >>>      torch.tensor([7., 8., 9.])]
    >>> attack(x)
    tensor([-8., -10., -12.])

    References
    ----------

    .. [1] Cong Xie, Oluwasanmi Koyejo, and Indranil Gupta. Fall of empires: Breaking byzantine-tolerant
            sgd by inner product manipulation. In Ryan P. Adams and Vibhav Gogate (eds.), Proceedings of
            The 35th Uncertainty in Artificial Intelligence Conference, volume 115 of Proceedings of Machine
            Learning Research, pp. 261–270. PMLR, 22–25 Jul 2020. URL https://proceedings.
            mlr.press/v115/xie20a.html.

    """

    def __init__(self, tau=3):
        self.tau = tau

    def __call__(self, honest_vectors):
        tools, honest_vectors = check_vectors_type(honest_vectors)
        mean_vector = tools.mean(honest_vectors, axis=0)
        return tools.multiply(mean_vector, 1 - self.tau)


class ALittleIsEnough():
    
    r"""
    Description
    -----------

    Execute the A Little is Enough (ALIE) attack [1]_: perturb the mean vector using the coordinate-wise standard deviation of the vectors multiplicatively scaled with the attack factor :math:`\tau`.

    .. math::

        \text{ALIE}_{\tau}(x_1, \dots, x_n) = \mu_{x_1, ..., x_n} + \tau \cdot \sigma_{x_1, ..., x_n}
    
    where

    - :math:`x_1, \dots, x_n` are the input vectors, which conceptually correspond to correct gradients submitted by honest participants during a training iteration.

    - :math:`\mu_{x_1, \dots, x_n} = \frac{1}{n}\sum_{i=1}^{n}x_i` is the mean vector.

    - \\(\\big[\\cdot\\big]_k\\) refers to the \\(k\\)-th coordinate.

    - :math:`\sigma_{x_1, \dots, x_n}` is the coordinate-wise standard deviation of :math:`x_1, \dots, x_n`, i.e., :math:`\big[\sigma_{x_1, \dots, x_n}\big]_k = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(\big[x_i\big]_k - \big[\mu_{x_1, \dots, x_n}\big]_k)^2}`.

    - :math:`\tau` is the attack factor.

    Initialization parameters
    --------------------------

    tau : int or float
        The attack factor :math:`\tau` used to adjust the mean vector. Set to 1.5 by default.

    Calling the instance
    --------------------

    Input parameters
    ----------------

    vectors: numpy.ndarray, torch.Tensor, list of numpy.ndarray or list of torch.Tensor
        A set of vectors, matrix or tensors.

    Returns
    -------
    :numpy.ndarray or torch.Tensor
        The data type of the output is the same as the input.
    
    Examples
    --------

    >>> import byzfl
    >>> attack = byzfl.ALittleIsEnough(1.5)

    Using numpy arrays:

    >>> import numppy as np
    >>> x = np.array([[1., 2., 3.], 
    >>>               [4., 5., 6.], 
    >>>               [7., 8., 9.]])
    >>> attack(x)
    array([ 8.5  9.5 10.5])
    
    Using torch tensors (Warning: We need the tensor to be either a floating point or complex dtype):
    
    >>> import torch
    >>> x = torch.stack([torch.tensor([1., 2., 3.]),
    >>>                  torch.tensor([4., 5., 6.]), 
    >>>                  torch.tensor([7., 8., 9.])])
    >>> attack(x)
    tensor([ 8.5000,  9.5000, 10.5000])

    Using list of numpy arrays

    >>> import numppy as np
    >>> x = [np.array([1., 2., 3.]),      # list of np.ndarray  
    >>>      np.array([4., 5., 6.]), 
    >>>      np.array([7., 8., 9.])]
    >>> attack(x)
    array([ 8.5  9.5 10.5])

    Using list of torch tensors (Warning: We need the tensor to be either a floating point or complex dtype):
        
    >>> import torch
    >>> x = [torch.tensor([1., 2., 3.]),  # list of torch.tensor 
    >>>      torch.tensor([4., 5., 6.]), 
    >>>      torch.tensor([7., 8., 9.])]
    >>> attack(x)
    tensor([ 8.5000,  9.5000, 10.5000])
   
    References
    ----------

    .. [1] Baruch, M., Baruch, G., and Goldberg, Y. A little is enough: Circumventing defenses for distributed learning.
           In Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, 8-14 December 2019, Long Beach, CA, USA, 2019.

    """

    def __init__(self, tau=1.5):
        self.tau = tau
    
    def __call__(self, honest_vectors):
        tools, honest_vectors = check_vectors_type(honest_vectors)
        attack_vector = tools.sqrt(tools.var(honest_vectors, axis=0, ddof=1))
        return tools.add(tools.mean(honest_vectors, axis=0),
                tools.multiply(attack_vector, self.tau))


class Mimic():
    
    r"""
    Description
    -----------

    Execute the Mimic attack [1]_: the attacker mimics the behavior of worker with ID :math:`\epsilon` by sending the same vector as that worker.

    .. math::

        \text{Mimic}_{\epsilon}(x_1, \dots, x_n) = x_{\epsilon+1}
    
    where

    - :math:`x_1, \dots, x_n` are the input vectors, which conceptually correspond to correct gradients submitted by honest participants during a training iteration.

    - :math:`\epsilon \in \{0, \dots, n-1\}` is the ID of the worker to mimic. In other words, :math:`x_{\epsilon+1}` is the vector sent by the worker with ID :math:`\epsilon`.

    Initialization parameters
    --------------------------

    epsilon : int
        ID of the worker whose behavior is to be mimicked. Set to 0 by default.

    Calling the instance
    --------------------

    Input parameters
    ----------------

    vectors: numpy.ndarray, torch.Tensor, list of numpy.ndarray or list of torch.Tensor
        A set of vectors, matrix or tensors.

    Returns
    -------
    :numpy.ndarray or torch.Tensor
        The data type of the output is the same as the input.
    
    Examples
    --------
    
    >>> import byzfl
    >>> attack = byzfl.Mimic(0)

    Using numpy arrays:

    >>> import numppy as np
    >>> x = np.array([[1., 2., 3.], 
    >>>               [4., 5., 6.], 
    >>>               [7., 8., 9.]])
    >>> attack(x)
    array([1. 2. 3.])

    Using torch tensors:

    >>> import torch
    >>> x = torch.stack([torch.tensor([1., 2., 3.]),
    >>>                  torch.tensor([4., 5., 6.]), 
    >>>                  torch.tensor([7., 8., 9.])])
    >>> attack(x)
    tensor([1., 2., 3.])

    Using list of numpy arrays

    >>> import numppy as np
    >>> x = [np.array([1., 2., 3.]),      # list of np.ndarray  
    >>>      np.array([4., 5., 6.]), 
    >>>      np.array([7., 8., 9.])]
    >>> attack(x)
    array([1.  2. 3.])

    Using list of torch tensors:

    >>> import torch
    >>> x = [torch.tensor([1., 2., 3.]),  # list of torch.tensor 
    >>>      torch.tensor([4., 5., 6.]), 
    >>>      torch.tensor([7., 8., 9.])]
    >>> attack(x)
    tensor([1., 2., 3.])

    References
    ----------

    .. [1] Sai Praneeth Karimireddy, Lie He, and Martin Jaggi. Byzantine-robust learning on heterogeneous datasets via bucketing. In International Conference on Learning Representations, 2022.
    
    """

    def __init__(self, epsilon=0):
        self.epsilon = epsilon
    
    def __call__(self, honest_vectors):
        return honest_vectors[self.epsilon]


class Inf():

    r"""
    Description
    -----------

    Execute the Infinity attack: send  vector :math:`\mathbf{v}_{\infty}` comprised of positive infinity values.

    .. math::

        \mathbf{v}_{\infty} = \begin{bmatrix} +\infty \\ +\infty \\ \vdots \\ +\infty \end{bmatrix} \in \mathbb{R}^d

    where

    - :math:`x_1, \dots, x_n` are the input vectors, which conceptually correspond to correct gradients submitted by honest participants during a training iteration.

    - :math:`d` is the dimensionality of the input space, i.e., :math:`d` is the number of coordinates of vectors :math:`x_1, \dots, x_n`.
    
    - Every coordinate of :math:`\mathbf{v}_{\infty}` is set to :math:`+\infty`.

    Initialization parameters
    --------------------------

    None

    Calling the instance
    --------------------

    Input parameters
    ----------------

    vectors: numpy.ndarray, torch.Tensor, list of numpy.ndarray or list of torch.Tensor
        A set of vectors, matrix or tensors.

    Returns
    -------
    :numpy.ndarray or torch.Tensor
        The data type of the output is the same as the input.

    Examples
    --------

    >>> import byzfl
    >>> attack = byzfl.Inf()

    Using numpy arrays:

    >>> import numppy as np
    >>> x = np.array([[1., 2., 3.], 
    >>>               [4., 5., 6.], 
    >>>               [7., 8., 9.]])
    >>> attack(x)
    array([inf, inf, inf])
    
    Using torch tensors:

    >>> import torch
    >>> x = torch.stack([torch.tensor([1., 2., 3.]),
    >>>                  torch.tensor([4., 5., 6.]), 
    >>>                  torch.tensor([7., 8., 9.])])
    >>> attack(x)
    tensor([inf, inf, inf])

    Using list of numpy arrays

    >>> import numppy as np
    >>> x = [np.array([1., 2., 3.]),      # list of np.ndarray  
    >>>      np.array([4., 5., 6.]), 
    >>>      np.array([7., 8., 9.])]
    >>> attack(x)
    array([inf, inf, inf])

    Using list of torch tensors (Warning: We need the tensor to be either a floating point or complex dtype):
        
    >>> import torch
    >>> x = [torch.tensor([1., 2., 3.]),  # list of torch.tensor 
    >>>      torch.tensor([4., 5., 6.]), 
    >>>      torch.tensor([7., 8., 9.])]
    >>> attack(x)
    tensor([inf, inf, inf])

    """ 

    def __init__(self):
        pass
    
    def __call__(self, honest_vectors):
        tools, honest_vectors = check_vectors_type(honest_vectors)
        return tools.full_like(honest_vectors[0], float('inf'), dtype=np.float64)
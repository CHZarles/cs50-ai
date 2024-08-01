Quiz 5

Question 1
Consider the below neural network, where we set:

w0 = -5
w1 = 2
w2 = -1 and
w3 = 3.
x1, x2, and x3 represent input neurons, and y represents the output neuron.

What value will this network compute for y given inputs x1 = 3, x2 = 2, and x3 = 4 if we use a step activation function? What if we use a ReLU activation function?

> The neural network be like

```
 1 -> Node--w0--|
x1 -> Node--w1--|
x2 -> Node--w2--|--> Node--g-> y
x3 -> Node--w3--|

g is a activation function

```

> represent in formula, given (1, 3, 2 ,3)
> g(w0 + w1 \* x1 + w2 \* x2 + w3 \* x3) = g(11)
> so the ans is:
> 1 for step activation function, 11 for ReLU activation function

Question 2
How many total weights (including biases) will there be for a fully connected neural network with a single input layer with 3 units, a single hidden layer with 5 units, and a single output layer with 4 units?

> In a fully connected neural network:
>
> - Every unit in the input layer is connected to every unit in the hidden layer.
> - Every unit in the hidden layer is connected to every unit in the output layer.
> - Each unit in the hidden and output layers also has a bias term.
>
> So, the total number of weights (including biases) can be calculated as follows:
>
> - Weights between the input layer and the hidden layer: 3 (input units) \* 5 (hidden units) = 15 weights
> - Biases in the hidden layer: 5 (one for each unit)
> - Weights between the hidden layer and the output layer: 5 (hidden units) \* 4 (output units) = 20 weights
> - Biases in the output layer: 4 (one for each unit)
>
> Adding these up, we get a total of 15 + 5 + 20 + 4 = 44 weights (including biases).

Question 3
Consider a recurrent neural network that listens to a audio speech sample, and classifies it according to whose voice it is. What network architecture is the best fit for this problem?

One-to-one (single input, single output)
Many-to-one (multiple inputs, single output)√

One-to-many (single input, multiple outputs)
Many-to-many (multiple inputs, multiple outputs)

Question 4
Consider a 4x4 grayscale image with the following pixel values.

Quiz 5, Question 4

What would be the result of applying a 2x2 max-pool to the original image?

(Note: Answers are formatted as a matrix [[a, b], [c, d]] where [a, b] is the first row and [c, d] is the second row.)

[[16, 12], [32, 28]]
[[16, 14], [32, 30]]
[[22, 24], [32, 30]]
[[14, 12], [30, 28]]
[[16, 14], [22, 24]]
[[16, 12], [32, 30]]

> [[16, 12], [32, 28]]

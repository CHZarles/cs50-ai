
## **Unconditional Probability**

Unconditional probability is the degree of belief in a proposition in the absence of any other evidence. 



## Conditional Probability

Conditional probability is the degree of belief in a proposition given some evidence that has already been revealed. 

Conditional probability is expressed using the following notation: 

$$P(a|b)$$



Mathematically, to compute the conditional probability of *a* given *b*, we use the following formula:

$$p(a|b) = \frac{p(a \cap b)}{p(b)}$$


## Random Variables

A random variable is a variable in probability theory with a domain of possible values that it can take on.


For example, to represent the status of a flight, we can define a variable *Flight* that takes on the values **{*on time, delayed, canceled*}.**


We represent this using a probability distribution. For example,

+   P(*Flight = on time*) = 0.6
+   P(*Flight = delayed*) = 0.3
+   P(*Flight = canceled*) = 0.1


### Independence

Independence is the knowledge that the occurrence of one event does not affect the probability of the other event.

Independence can be defined mathematically, events *a* and *b* are independent if and only if:

$$P(a \land b) = P(a)P(b)$$


## Bayes’ Rule

Bayes’ rule is commonly used to compute conditional probability.

$$P(a|b) = \frac{P(b|a)P(a)}{P(b)}$$

## Joint Probability

Joint probability is the likelihood of multiple events all occurring.

Let us consider the following example,concerning the probabilities of:
- clouds in the morning 

| C = *cloud* | C = *¬cloud* |
| --- | --- |
| 0.4 | 0.6 |

- rain in the afternoon.

| R = *rain* | R = *¬rain* |
| --- | --- |
| 0.1 | 0.9 |


joint probabilities of all the possible outcomes of the two variables. We can represent this in a table as follows:

|   | R = *rain* | R = *¬rain* |
| --- | --- | --- |
| C = *cloud* | 0.08 | 0.32 |
| C = *¬cloud* | 0.02 | 0.58 |


Using joint probabilities, we can deduce conditional probability. 

For example, if we are interested in the **probability distribution of clouds in the morning given rain in the afternoon.**


$$p(C|rain) = \frac{p(C \cap rain)}{p(rain)}=α<0.08, 0.02> = 1$$

then we got 

$$α = 1$$
$$p(C|rain) = <0.8, 0.2>$$


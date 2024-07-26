# Intro of this course

## Welcome

This course explores the concepts and algorithms at the foundation of modern artificial intelligence, diving into the ideas that give rise to technologies like game-playing engines, handwriting recognition, and machine translation. Through hands-on projects, students gain exposure to the theory behind graph search algorithms, classification, optimization, machine learning, large language models, and other topics in artificial intelligence as they incorporate them into their own Python programs. By course’s end, students emerge with experience in libraries for machine learning as well as knowledge of artificial intelligence principles that enable them to design intelligent systems of their own.

Prerequisites

[CS50x](https://cs50.harvard.edu/x) or at least one year of experience with Python.

Watch an introduction

## How to Take this Course

Even if you are not a student at Harvard, you are welcome to “take” this course for free via this OpenCourseWare by working your way through the course’s seven [weeks](https://cs50.harvard.edu/ai/2024/weeks/) of material. If you’d like to submit the course’s seven [projects](https://cs50.harvard.edu/ai/2024/projects/) for feedback, be sure to [create an edX account](https://courses.edx.org/register), if you haven’t already. Ask questions along the way via any of the course’s [communities](https://cs50.harvard.edu/ai/2024/communities/)!

- If interested in a [verified certificate](https://www.edx.org/verified-certificate) from [edX](https://www.edx.org/), enroll at [cs50.edx.org/ai](https://cs50.edx.org/ai) instead.
- If interested in a [professional certificate](https://www.edx.org/professional-certificate) from [edX](https://www.edx.org/), enroll at [cs50.edx.org/programs/ai](https://cs50.edx.org/programs/ai) instead.
- If interested in [transfer credit and accreditation](https://extension.harvard.edu/for-students/student-policies-conduct/transfer-credits-accreditation/) from [Harvard Extension School](https://www.extension.harvard.edu/), register at [web.dce.harvard.edu/extension/csci/e/80](https://web.dce.harvard.edu/extension/csci/e/80) instead.
- If interested in [transfer credit and accreditation](https://summer.harvard.edu/academic-opportunities-support/policies-and-regulations/academic-policies/transfer-credit-accreditation/) from [Harvard Summer School](https://www.summer.harvard.edu/), register at [web.dce.harvard.edu/summer/csci/s/80](https://web.dce.harvard.edu/summer/csci/s/80) instead.

## How to Teach this Course

If you are a teacher, you are welcome to adopt or adapt these materials for your own course, per the [license](https://cs50.harvard.edu/ai/2024/license/).

# Search

- source url:
  - https://cs50.harvard.edu/ai/2024/projects/0/degrees/
  - https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/

reference

- [ 机器人路径规划算法（十一）A-star算法 ] (https://mronne.github.io/2020/04/03/%E6%9C%BA%E5%99%A8%E4%BA%BA%E8%B7%AF%E5%BE%84%E8%A7%84%E5%88%92%E7%AE%97%E6%B3%95-%E5%8D%81%E4%B8%80-A-star-%E7%AE%97%E6%B3%95.html)

# knowledge

- source url
  - https://cs50.harvard.edu/ai/2024/projects/1/knights/
    - mark: 这个project主要是训练用 Proposition 表达 knowledge base 的能力 ? 最后一个puzzle比较难，虽然过了case。。感觉还是不是很理解
  - https://cs50.harvard.edu/ai/2024/projects/1/minesweeper/

# Probability

- source url

  - https://cs50.harvard.edu/ai/2024/projects/2/pagerank/
  - https://cs50.harvard.edu/ai/2024/projects/2/heredity/

- core conception

  - Some rule ( math tool )

    - conditional Probability
    - Joint Probability
    - Bayesian rule
    - Probability rule

      - negative
      - Marginalization
      - ...

    - Bayesion Network

      - an efficient way to represent any full joint probability distribution by exploiting conditional independence
      - Inference
        - exact Inference:
          - use math rule, enumeration, variable elimination
        - approximate inference:
          - sampling methods

    - Probabilistic reasoning over time
      - (hidden) Markov model , Markov chains
      - sensor model , transition model

- complementary reference
  - https://ktiml.mff.cuni.cz/~bartak/ui2/lectures/

# optimization

- source url

  - https://cs50.harvard.edu/ai/2024/projects/3/crossword/

- Core conception
  - Local search
    - Hill climbing
      - Simulated Annealing
  - Linear Programming
  - Constraint Satisfaction
    - terms of constraint
      - unary constraint
        - Node Consistency
      - binary constraint
        - Arc Consistency
      - Hard / soft constraint
    - revise algorithm
    - arc3 algorithm
    - backtrack search algorithm

# Machine learning

- Core conception
  - Supervised learning
    - learn a function to map input to output
    - relative task
      - classification
        - nearest-neighbour classification
        - k-nearest-neighbour classification
        - perceptron learning rule
          - define , weight vector / input vector
            - W dot product X -> Output
          - update a formulation
            - update each weight given data point, (x , y)
              - ie. wi = wi + α(actual_value - estimate) \* xi
                - α is learning rate , a number which we choose
          - end up with a threshold function
        - Support Vector Machines
          - effect: maximum margin separator
            - boundary that maximizes the distance between any of the data points
            - can represent decision boundaries with more than two dimensions
      - regression
        - learning a function mapping an input point to a continuous value
    - Evaluating Hypotheses
      - loss function : expresses how poorly our hypothesis performs
        - 0-1 loss function
        - L1 loss function
        - L2 loss function
      - overfitting : a model that fits too closely to particular data set
        - define cost function, cost(h) = loss(h) + complexity(h)
        - avoid overfitting:
          - regularization : penalizing hypothesis that are more complex to favor simpler, more general Hypotheses
          - holdout cross-validation
            - splitting data into a training set and test set
  - Reinforcement learning
    - define: given a set of rewards or punishments, learn what actions to take the future.
    - Markov Decision Process
      - Set of states S
      - Set of actions Actions(s)
      - Transition model P(s'|s,a)
      - Reward function R(s, a,'s)
    - Q-learning

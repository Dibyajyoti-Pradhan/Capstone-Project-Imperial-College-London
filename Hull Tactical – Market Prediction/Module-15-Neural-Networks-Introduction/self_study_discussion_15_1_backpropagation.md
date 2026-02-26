# Self-Study Discussion 15.1: Replicate the Backpropagation Example

---

## Part 1: Forward and Backward Pass

### Computation Graph

From the given graph, we have the following nodes:

- **c₁ = a × b** (multiplication)
- **c₂ = max(a, 2)** (max function)
- **c₃ = c₁ + c₂** (addition)
- **c₄ = ln(c₃)** (natural logarithm)

---

### Forward Pass

Computing intermediate values from left to right:

$$c_1 = a \cdot b$$

$$c_2 = \max(a, 2) = \begin{cases} a & \text{if } a > 2 \\ 2 & \text{if } a \leq 2 \end{cases}$$

$$c_3 = c_1 + c_2 = ab + \max(a, 2)$$

$$c_4 = \ln(c_3) = \ln(ab + \max(a, 2))$$

**Final Output:**

$$\boxed{c_4 = \ln(ab + \max(a, 2))}$$

---

### Backward Pass

We compute $\frac{dc_4}{da}$ by applying the chain rule from right to left.

**Step 1: Derivative of the logarithm node**

$$\frac{\partial c_4}{\partial c_3} = \frac{1}{c_3}$$

**Step 2: Derivative of the addition node**

$$\frac{\partial c_3}{\partial c_1} = 1 \quad \text{and} \quad \frac{\partial c_3}{\partial c_2} = 1$$

**Step 3: Derivative of the multiplication node**

$$\frac{\partial c_1}{\partial a} = b$$

**Step 4: Derivative of the max node**

$$\frac{\partial c_2}{\partial a} = \frac{\partial}{\partial a} \max(a, 2) = \begin{cases} 1 & \text{if } a > 2 \\ 0 & \text{if } a < 2 \\ \text{undefined} & \text{if } a = 2 \end{cases}$$

**Step 5: Apply the chain rule**

Since $a$ flows to $c_4$ through two branches ($c_1$ and $c_2$), we sum the contributions:

$$\frac{dc_4}{da} = \frac{\partial c_4}{\partial c_3} \cdot \left( \frac{\partial c_3}{\partial c_1} \cdot \frac{\partial c_1}{\partial a} + \frac{\partial c_3}{\partial c_2} \cdot \frac{\partial c_2}{\partial a} \right)$$

Substituting:

$$\frac{dc_4}{da} = \frac{1}{c_3} \cdot \left( 1 \cdot b + 1 \cdot \frac{\partial c_2}{\partial a} \right)$$

$$\frac{dc_4}{da} = \frac{1}{ab + \max(a,2)} \cdot \left( b + \mathbb{1}_{[a > 2]} \right)$$

**Final Gradient:**

$$\boxed{\frac{dc_4}{da} = \begin{cases} \displaystyle\frac{b + 1}{ab + a} = \frac{b+1}{a(b+1)} = \frac{1}{a} & \text{if } a > 2 \\[12pt] \displaystyle\frac{b}{ab + 2} & \text{if } a < 2 \\[12pt] \text{undefined} & \text{if } a = 2 \end{cases}}$$

---

## Part 2: Reflection Questions

### 1. Where in the graph does the non-differentiability arise?

The non-differentiability occurs at the **max(a, 2) node** when **a = 2**.

At this point, the function $\max(a, 2)$ has a sharp corner where the derivative abruptly jumps from 0 to 1:

$$\lim_{a \to 2^-} \frac{\partial c_2}{\partial a} = 0 \quad \neq \quad \lim_{a \to 2^+} \frac{\partial c_2}{\partial a} = 1$$

This is analogous to the non-differentiability of ReLU at zero, which is ubiquitous in neural networks.

---

### 2. How does the choice of value for $a$ affect the flow of gradients?

The value of $a$ acts as a **gate** controlling gradient flow through the $c_2$ branch:

| Condition | Gradient through $c_1$ branch | Gradient through $c_2$ branch | Total $\frac{dc_4}{da}$ |
|-----------|------------------------------|------------------------------|------------------------|
| $a > 2$ | $\frac{b}{c_3}$ | $\frac{1}{c_3}$ | $\frac{b+1}{c_3}$ |
| $a < 2$ | $\frac{b}{c_3}$ | **0** (blocked) | $\frac{b}{c_3}$ |

When $a < 2$, the max node outputs a constant (2), so $\frac{\partial c_2}{\partial a} = 0$, effectively **killing the gradient** through that path. This mirrors the "dying ReLU" problem in deep networks.

---

### 3. Why is it helpful to break complex expressions into intermediate steps?

Breaking $c_4 = \ln(ab + \max(a,2))$ into nodes $c_1, c_2, c_3, c_4$ provides:

1. **Simplified local derivatives:** Each node requires only elementary calculus ($\frac{d}{dx}\ln(x) = \frac{1}{x}$, $\frac{d}{dx}(x \cdot y) = y$)

2. **Efficient computation:** Forward pass values are cached and reused in the backward pass

3. **Automatic differentiation compatibility:** This decomposition is exactly how PyTorch and TensorFlow implement backpropagation via computational graphs

4. **Debugging clarity:** Identifies exactly where gradients vanish or explode

---

### 4. Which method — forward or backward — was more intuitive for you, and why?

**Forward pass** is more intuitive for understanding the function's behaviour — it follows the natural flow of computation from inputs to outputs.

**Backward pass** is more intuitive for understanding optimisation — it reveals how each intermediate variable contributes to the final output. For neural networks with $n$ parameters and a single scalar loss, backward mode computes all $n$ gradients in $O(1)$ backward passes, whereas forward mode would require $O(n)$ passes.

For this problem, the backward pass clarified how the max node creates conditional gradient flow — insight that would be obscured in a direct analytical differentiation.


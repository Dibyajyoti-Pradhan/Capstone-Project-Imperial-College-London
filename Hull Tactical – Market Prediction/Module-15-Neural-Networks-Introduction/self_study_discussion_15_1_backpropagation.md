# Self-Study Discussion 15.1: Replicate the Backpropagation Example

## Part 1: Forward and Backward Pass

### Computation Graph

```
        b
        │
    ┌───┴───┐
a ──┤   ×   ├──► c₁ ──┐
    └───────┘         │
                      ├──► c₃ ──► ln ──► c₄
    ┌───────┐         │
a ──┤ max(,2)├──► c₂ ──┘
    └───────┘
```

### Forward Pass

Computing intermediate values left to right:

| Node | Expression | Value |
|------|------------|-------|
| c₁ | a × b | ab |
| c₂ | max(a, 2) | a if a > 2, else 2 |
| c₃ | c₁ + c₂ | ab + max(a, 2) |
| c₄ | ln(c₃) | ln(ab + max(a, 2)) |

**Final output:** c₄ = ln(ab + max(a, 2))

### Backward Pass

Applying the chain rule from right to left to compute dc₄/da:

**Step 1: Log node derivative**
```
∂c₄/∂c₃ = 1/c₃
```

**Step 2: Addition node derivatives**
```
∂c₃/∂c₁ = 1
∂c₃/∂c₂ = 1
```

**Step 3: Branch derivatives with respect to a**
```
∂c₁/∂a = b                    (multiplication rule)
∂c₂/∂a = 1 if a > 2, 0 if a < 2, undefined at a = 2
```

**Step 4: Combine using chain rule**

Since a affects c₄ through two paths (c₁ and c₂):

```
dc₄/da = (∂c₄/∂c₃) × [(∂c₃/∂c₁ × ∂c₁/∂a) + (∂c₃/∂c₂ × ∂c₂/∂a)]

dc₄/da = (1/c₃) × [b + 𝟙(a > 2)]
```

**Final gradient:**

| Condition | dc₄/da |
|-----------|--------|
| a > 2 | (b + 1) / (ab + a) |
| a < 2 | b / (ab + 2) |
| a = 2 | Undefined |

---

## Part 2: Reflection Questions

### 1. Where does non-differentiability arise?

At the **max(a, 2) node** when **a = 2**. The max function creates a "kink" where the output switches from the constant 2 to the variable a. This mirrors the non-differentiability of ReLU at zero — both are piecewise linear functions with a sharp transition point.

### 2. How does the choice of a affect gradient flow?

The value of a acts as a **gate** for the c₂ branch:
- **a > 2:** Both branches contribute to the gradient (b + 1 in numerator)
- **a < 2:** The max branch is "dead" — outputs constant 2, so ∂c₂/∂a = 0, blocking gradient flow through that path

This illustrates how certain neurons can become inactive during training, a phenomenon known as the "dying ReLU" problem in deep learning.

### 3. Why break complex expressions into intermediate steps?

Three key benefits:
- **Modularity:** Each node has a simple local derivative, avoiding messy nested differentiation
- **Reusability:** Intermediate values computed in the forward pass are reused in the backward pass
- **Debugging:** Isolates where gradients vanish or explode, making it easier to diagnose training issues

This decomposition is exactly how automatic differentiation frameworks (PyTorch, TensorFlow) implement backpropagation efficiently.

### 4. Which method was more intuitive — forward or backward?

**Forward pass** is more intuitive for understanding *what* the function computes — it follows natural cause-and-effect.

**Backward pass** is more intuitive for understanding *how* to optimise — it reveals each component's contribution to the output. For neural networks with millions of parameters but a single loss value, backward mode is computationally essential: one backward pass computes all gradients simultaneously.


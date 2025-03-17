# Fama-French-Model-Template-for-Testing
This repo contains different Fama French model to test a stocks for factor exposure analysis

The goal of this project is to analyze stock returns by decomposing them into key risk factors (market, size, value, profitability, investment, momentum). This helps to understand why a stock performs the way it does and whether its return is driven by systematic risk factors or unexplained alpha.

The **Fama-French models** are extensions of the **Capital Asset Pricing Model (CAPM)**. They introduce additional factors to explain stock returns more effectively.

##   1️. Fama-French 3-Factor Model  

The **3-factor model** extends CAPM by adding **size (SMB)** and **value (HML)** factors:

$$
R_i - R_f = \alpha + \beta_m (R_m - R_f) + \beta_s \text{SMB} + \beta_h \text{HML} + \epsilon
$$

### **Explanation of Terms:**
- $R_i$ = Return of stock $i$
- $R_f$ = Risk-free rate (e.g., 3-month T-Bill)
- $R_m$ = Return of the market (e.g., S&P 500)
- $\alpha$ = Stock-specific alpha (excess return not explained by the model)
- $\beta_m$ = Market beta (sensitivity to overall market movements)
- **SMB (Small Minus Big)** = Return spread between small-cap and large-cap stocks  
- **HML (High Minus Low)** = Return spread between high and low book-to-market (value vs. growth stocks)  
- $\epsilon$ = Residual error term  


---

##  2️. Fama-French 5-Factor Model 

The **5-factor model** further improves the explanation of returns by introducing **profitability (RMW)** and **investment (CMA)** factors:

$$
R_i - R_f = \alpha + \beta_m (R_m - R_f) + \beta_s \text{SMB} + \beta_h \text{HML} + \beta_r \text{RMW} + \beta_c \text{CMA} + \epsilon
$$

### **Additional Factors:**
- **RMW (Robust Minus Weak)** = Return spread between high-profitability and low-profitability firms  
- **CMA (Conservative Minus Aggressive)** = Return spread between firms with conservative and aggressive investment policies  

 
- The **5-factor model** suggests that the **HML (value factor)** may be redundant because it overlaps with RMW and CMA.

---

## 3. Fama-French 6-Factor Model 

The **6-factor model** introduces a **momentum factor (UMD)** to capture the tendency of past winners to keep winning:

$$
R_i - R_f = \alpha + \beta_m (R_m - R_f) + \beta_s \text{SMB} + \beta_h \text{HML} + \beta_r \text{RMW} + \beta_c \text{CMA} + \beta_m \text{UMD} + \epsilon
$$

### **Momentum Factor:**
- **UMD (Up Minus Down)** = Return spread between stocks with high past returns (winners) and low past returns (losers)  

 
---

## **Summary of Factor Models**
| Model | Factors Included |
|--------|----------------|
| **CAPM** | Market risk ($$ R_m - R_f $$) |
| **Fama-French 3-Factor** | Market, SMB (Size), HML (Value) |
| **Fama-French 5-Factor** | Market, SMB, HML, RMW (Profitability), CMA (Investment) |
| **Fama-French 6-Factor** | Market, SMB, HML, RMW, CMA, UMD (Momentum) |

---




## How to interpret OLS results:

1. R-squared:
    * Explains how much of the stock’s excess return is captured by the model.
    * Higher R² (closer to 1) → The model does a better job of explaining returns. (>0.7)

### Coeff below needs to have P-value < 0.05 to be statistically significant
2. Mkt-RF Coeff (Beta):
    * Measures how much the stock moves in relation to the market (S&P 500).
    * High Beta (>1) → The stock is more volatile than the market.
3. Size Factor Coeff (SMB - Small Minus Big):
    * Positive SMB → The stock behaves like a small-cap stock.
        * Above 0.2 → More exposure to small-cap stocks.
        * Between -0.2 and 0.2 → Neutral (doesn’t behave like either).
        * Below -0.2 → Large-cap characteristics.
4. Value Factor (HML - High Minus Low)
    * Positive HML → The stock behaves like a value stock.
        * Above 0.3 → More exposure to value stocks.
        * Between -0.3 and 0.3 → Neutral.
        * Below -0.3 → More exposure to growth stocks.

5. Profitability Factor (RMW - Robust Minus Weak)
    * Positive RMW → The company is highly profitable.
    * Negative RMW → The company is low profitability.
        * Above 0.2 → High-profitability companies.
        * Between -0.2 and 0.2 → Neutral.
        * Below -0.2 → Weak profitability.

6. Investment Factor (CMA - Conservative Minus Aggressive)
    * Positive CMA → The company follows a conservative investment strategy.
        * Above 0.2 → Conservative investment strategy (steady growth).
        * Between -0.2 and 0.2 → Neutral.
        * Below -0.2 → Aggressive investment strategy.

7. Momentum Factor (UMD - Up Minus Down)
    * Positive UMD → The stock follows momentum (winners keep winning).
    * Negative UMD → The stock has mean-reverting behavior.
        * Above 0.2 → Strong momentum effect.
        * Between -0.2 and 0.2 → No strong momentum.
        * Below -0.2 → Tends to mean revert.

8. Constant (const): Alpha
 
    * Measures abnormal returns that cannot be explained by the factors.
    * If significant (p < 0.05) → The stock has unexplained alpha.


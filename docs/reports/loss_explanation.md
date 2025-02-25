# Power Loss Analysis: Time Series vs Static Simulation

## 1. Fundamental Differences

### Static (Single Snapshot) Analysis
- Uses fixed load values
- Represents one specific operating point
- Total losses from OpenDSS master file represent losses at nominal loading

### Time Series Analysis
- Variable load values throughout the day
- 24 different operating points
- Losses change quadratically with current (I²R relationship)

## 2. Loss Variation Factors

### Load-Dependent Losses
1. **I²R Relationship**
   - Power losses are proportional to the square of current
   - When load is at 50% of nominal:
     * Current is approximately 50% of nominal
     * Losses are approximately 25% of nominal
   - This non-linear relationship explains why average daily losses ≠ nominal case losses

2. **Daily Load Pattern Impact**
   - Peak hours (11:00, 18:00): 100% load → 100% of nominal losses
   - Minimum load (04:00): 55% load → ~30% of nominal losses
   - Average daily load: ~80% → ~64% of nominal losses

### Voltage-Dependent Effects
1. **System Voltage Variations**
   - Lower voltage → Higher current for same power
   - Higher current → Increased losses
   - Voltage profile changes with loading

2. **Reactive Power Flow**
   - Different loading conditions affect reactive power flow
   - Changes in power factor impact total losses
   - Reactive compensation effectiveness varies with loading

## 3. Mathematical Explanation

### Loss Calculation
For a simple resistive element:
```
P_loss = I² × R
       = (S / V)² × R
       = (P² + Q²) / V² × R
```
Where:
- P_loss: Power loss
- I: Current
- R: Resistance
- S: Apparent power
- V: Voltage
- P: Active power
- Q: Reactive power

### Time Series Impact
1. **Hourly Loss Variation**
   ```
   For hour h:
   P_loss(h) = (LoadMultiplier(h))² × Nominal_Loss
   ```

2. **Daily Average Loss**
   ```
   Average_Loss = Σ(P_loss(h)) / 24
                ≠ Nominal_Loss
   ```

## 4. Example Calculation

### Static Case (100% Loading)
- Nominal load: 100%
- Nominal loss: Let's say 1000 kW

### Time Series Cases
1. **Peak Hours (Load = 100%)**
   - Loss = 1000 kW (same as nominal)

2. **Off-Peak (Load = 55%)**
   - Loss = (0.55)² × 1000 = 302.5 kW

3. **Average Daily Loss**
   ```
   Average = Σ((LoadMultiplier(h))² × Nominal_Loss) / 24
   ```
   This will be less than nominal loss due to the quadratic relationship.

## 5. Implications for Analysis

### System Planning
1. **Peak Capacity**
   - Must consider maximum losses during peak load
   - Critical for equipment rating

2. **Energy Efficiency**
   - Daily average losses more relevant
   - Important for economic analysis

### Operational Considerations
1. **Loss Minimization**
   - Different strategies needed for different loading conditions
   - Optimal control settings may vary throughout the day

2. **Equipment Loading**
   - Dynamic ratings might be applicable
   - Cooling requirements vary with loading

## 6. Recommendations for Analysis

1. **For Planning Studies**
   - Use time series analysis for accurate loss estimation
   - Consider both peak and average conditions

2. **For Operations**
   - Monitor loss patterns throughout the day
   - Adjust control settings based on loading

3. **For Economic Analysis**
   - Use time series results for energy loss calculations
   - Consider time-of-use pricing impacts 
"""
Market Microstructure Feature Engineering Module: High-Frequency Metrics.

This module serves as Layer 2 of the alpha-engine quantitative framework. It 
ingests real-time and historical transaction-level data streams from exchange 
matching engines (Layer 1) and transforms raw tick fields into vectorized, 
statistically viable alpha features for machine learning models (Layer 3).

Core Features Implemented:
--------------------------
1. Cumulative Volume Delta (CVD)
   Tracks the continuous running sum of aggressive volume delta. It isolates 
   the execution footprints of liquidity takers (market orders) while ignoring 
   passive liquidity providers (limit orders). Used to detect institutional 
   accumulation, bearish absorption, and structural volume divergences.

Mathematical Framework:
----------------------
For each transaction tick $i$ with executed volume $V_i$:
    Let Aggressor = BUY  => \Delta V_i = +V_i  (Aggressive Market Buy)
    Let Aggressor = SELL => \Delta V_i = -V_i  (Aggressive Market Sell)

The Cumulative Volume Delta (CVD) at step $t$ is formulated as:
    CVD_t = \sum_{i=1}^{t} \Delta V_i

Design Patterns & Computational Efficiency:
-----------------------------------------
* Stateful Streaming: Maintains a localized internal memory footprint 
  (running_cvd) to dynamically compute incoming tick updates in O(1) time.
* Vectorized Batching: Employs fast NumPy/Pandas array mappings (np.where) 
  to execute matrix-wide cumulative additions over cached DataFrames, 
  avoiding iterative Python loops and optimizing time-to-market calculations.

Usage:
------
    from src.features.metrics import HighFrequencyMetrics
    
    # Initialize stateful feature engine
    metrics_engine = HighFrequencyMetrics()
    
    # Update on streaming WebSocket packet
    current_cvd = metrics_engine.update_cvd(aggressor="BUY", quantity=0.452)
"""

import pandas as pd
import numpy as np

class HighFrequencyMetrics:
    def __init__(self):
        """
        Stateful engine to compute microstructural features from
        streaming market data packets.
        """
        self.running_cvd = 0.0

    def update_cvd(self, aggressor: str, quantity: float) -> float:
        """
        Updates and returns the running Cumulative Volume Delta (CVD).

        Parameters:
        aggressor (str): "BUY" or "SELL" indicating the taker market order directorino
        quantity (float): the size/volume of the executed trade packet.
    
        """
        if aggressor == "BUY":
            volume_delta = quantity
        elif aggressor == "SELL":
            volume_delta = -quantity
        else:
            volume_delta = 0.0

        self.running_cvd += volume_delta
        return self.running_cvd

    def process_batch_cvd(self, df: pd.DataFrame) -> pd.Series:
        """
        Vectorized batch calculation of CVD for historical/cached DataFrames
        Expects columns: 'agressor' and 'quantity'
        """
        # Assign positive volume to BUY market orders, negative to SELL market orders
        volume_deltas = np.where(df['aggressor'] == 'BUY', df['quantity'], -df['quantity'])

        # Compute the cumulative sum across the matrix array
        batch_cvd = pd.Series(volume_deltas).cumsum() + self.running_cvd

        # Update internal state with the last calculated value
        if not batch_cvd.empty:
            self.running_cvd = batch_cvd.iloc[-1]

        return batch_cvd


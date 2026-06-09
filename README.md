# Alpha Engine: Institutional-Grade Quantitative Research Framework

`alpha-engine` is a modular, high-performance financial engineering and market microstructure platform designed to extract, transform, and model high-frequency order book data.

The system decouples real-time data ingestion pipelines from mathematical feature engineering, providing a pristine, reproducible sandbox for developing statistical trading alpha.

The framework is constructed from first principles using modern, high-velocity tools to ensure sub-millisecond execution and complete computational determinism.

---

## 🏗️ System Architecture

The engine is engineered around a strict separation of concerns, divided into three computational layers:

```text
   [LAYER 3: CENTRAL EXECUTION CORE]
   (Predictive Models, Anomaly Detection)
                     ▲
                     │
 [LAYER 2: ALGORITHMIC FEATURE ENGINE]
 (Order Flow Imbalance, Cumulative Vol Delta)
                     ▲
                     │
 [LAYER 1: SYSTEM ASYNC PLUMBING NODE]
 (Low-Latency WebSockets, Ingestion Engines)
```

### Layer 1: Pipeline Ingestion (`src/pipeline/`)

- Establishes resilient, non-blocking, asynchronous WebSocket connections to exchange matching engines.
- Parses unstructured network JSON payloads into highly compressed, normalized data packets.

### Layer 2: Features Engine (`src/features/`)

- Transforms raw transaction ticks into vectorized statistical features.
- Implements market microstructure metrics including:
  - **Order Flow Imbalance (OFI)**
  - **Cumulative Volume Delta (CVD)**

### Layer 3: Execution Core (`src/main.py`)

- Fuses high-frequency technical signals with systematic risk parameters.
- Provides a centralized environment for signal generation, validation, and capital allocation logic.

---

## ⚡ Tech Stack & Core Dependencies

This framework utilizes modern infrastructure to eliminate environment drift and optimize execution loops:

| Component | Technology |
|------------|------------|
| Runtime & Package Management | `uv` |
| Asynchronous Networking | `websockets` |
| Data Processing | `pandas`, `numpy` |

### Runtime & Package Virtualization

- **uv** — Blazing-fast, Rust-powered Python package resolver and environment manager.

### Asynchronous Networking

- **websockets** — Low-overhead, event-driven networking for real-time order book monitoring.

### Vectorized Data Arrays

- **pandas** & **numpy** — C-optimized numerical computing libraries for high-density statistical calculations.

---

## 🚀 Getting Started

### 1. Clone and Initialize Environment

Ensure you have `uv` installed on your machine.

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/alpha-engine.git
cd alpha-engine

# Install and lock dependencies
uv sync
```

### 2. Run the Live Ingestion Pipeline

Launch the real-time market data listener:

```bash
uv run src/pipeline/streamer.py
```

This will connect to the exchange feed and begin streaming live order flow telemetry.

---

## 📊 Core Engineered Metrics

### 🛡️ Order Flow Imbalance (OFI)

Order Flow Imbalance measures net changes in supply and demand at the best bid and ask levels before price movements become visible on traditional charts.

:contentReference[oaicite:0]{index=0}

**Tracks:**

- Limit order additions
- Order cancellations
- Liquidity absorption
- Short-term directional pressure

---

### 🌊 Cumulative Volume Delta (CVD)

CVD aggregates the difference between aggressive market buy volume and aggressive market sell volume over time.

**Used to identify:**

- Institutional accumulation
- Distribution phases
- Divergences between price and participation
- Hidden market pressure

---

## 📂 Project Structure

```text
alpha-engine/
│
├── src/
│   ├── pipeline/
│   │   └── streamer.py
│   │
│   ├── features/
│   │   ├── ofi.py
│   │   └── cvd.py
│   │
│   └── main.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 📜 License

This project is distributed under the **MIT License**.

Built for rigorous quantitative research, market microstructure analysis, and systematic alpha development.

---

## 📦 Commit Changes

After updating the documentation:

```bash
git add README.md
git commit -m "docs: populate framework readme with system specifications"
git push
```

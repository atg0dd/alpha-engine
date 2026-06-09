import asyncio
import json
import websockets
from datetime import datetime
from src.features.metrics import HighFrequencyMetrics

class AlphaEngineCore:
    def __init__(self, symbol='btcusdt'):
        self.symbol = symbol.lower()
        self.uri = f"wss://fstream.binance.com/ws/{self.symbol}@aggTrade"
        self.metrics_engine = HighFrequencyMetrics()

    async def start_orchestration_loop(self):
        print(f"[*] Activating Core Orchestration Engine for symbol: {self.symbol.upper()}")
        print("[*] Synchronizing network sockets with feature engineering pipelines...")

        while True: 
            try:
                async with websockets.connect(self.uri) as websocket:
                    print("[+] System Convergence Achieved: Straming live order flow telemetry.")

                    while True:
                        # Non-blocking network packet ingestion
                        raw_packet = await websocket.recv()
                        packet = json.loads(raw_packet)

                        # Route decoded packet directly into the execution loop
                        self.orchestrate_event(packet)
                
            except websockets.exceptions.ConnectionClosed:
                print("[-] Network pipe disconnected by exchange host. Retrying core orchestration loop...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"[-] Critical execution loop exception: {e}")
                await asyncio.sleep(5)

    def orchestrate_event(self, packet):
        """
        Coordinates events across system boundaries. Decodes data packets
        and mutates feature tracking states simultaneously.
        """
        # Layer 1: Extraction & Normalization
        timestamp = datetime.fromtimestamp(packet['T'] / 1000.0)
        price = float(packet['p'])
        quantity = float(packet['q'])
        is_buyer_maker = packet['m']
        aggressor = "SELL" if is_buyer_maker else "BUY"

        # Layer 2: Mathematical Feature Transformation
        # Direct state mutation of the CVD array
        current_cvd = self.metrics_engine.update_cvd(aggressor, quantity)

        # Layer 3: Telemetry Stream Dashboard
        # In production, these variables feed directly into machine learning weights
        print(
            f"[{timestamp.strftime('%H:%M:%S.%f')[:-3]}] "
            f"Taker: {aggressor:4} | "
            f"Price: ${price:,.2f} | "
            f"Trade Qty: {quantity:8.4f} | "
            f"Engine CVD: {current_cvd:+12.4f}",
            flush=True
        )

if __name__ == "__main__":
    # Instantiate the system pipeline blueprint
    core_engine = AlphaEngineCore(symbol="btcusdt")
    
    try:
        asyncio.run(core_engine.start_orchestration_loop())
    except KeyboardInterrupt:
        print("\n[-] Alpha Engine systematically powered down. Memory cache cleared cleanly.")








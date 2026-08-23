// Real-time WebSocket Telemetry Handler
class WebSocketClient {
  constructor() {
    this.ws = null;
    this.pingInterval = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 10;
  }

  connect() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/live-stats`;

    console.log("🔌 Connecting to FastAPI WebSocket:", wsUrl);
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log("⚡ WebSocket Connected to FastAPI live telemetry!");
      this.reconnectAttempts = 0;
      this.updateStatusPill(true);
      this.startPing();
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      } catch (err) {
        console.warn("WebSocket non-JSON payload:", event.data);
      }
    };

    this.ws.onclose = () => {
      console.log("🔌 WebSocket Disconnected.");
      this.updateStatusPill(false);
      this.stopPing();
      this.attemptReconnect();
    };

    this.ws.onerror = (err) => {
      console.error("WebSocket Error:", err);
    };
  }

  handleMessage(data) {
    if (data.type === "visitor_count" || data.type === "handshake") {
      const visitorsEl = document.getElementById("active-visitors-count");
      if (visitorsEl && data.active_visitors !== undefined) {
        visitorsEl.textContent = data.active_visitors;
      }
    }

    if (data.type === "pong") {
      const latencyEl = document.getElementById("ws-latency");
      if (latencyEl && this.lastPingTime) {
        const rtt = Math.round(performance.now() - this.lastPingTime);
        latencyEl.textContent = `${rtt}ms`;
      }
    }
  }

  startPing() {
    this.stopPing();
    this.pingInterval = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.lastPingTime = performance.now();
        this.ws.send(JSON.stringify({ command: "ping" }));
      }
    }, 5000);
  }

  stopPing() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = null;
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      setTimeout(() => this.connect(), delay);
    }
  }

  updateStatusPill(online) {
    const pill = document.getElementById("server-status-pill");
    if (pill) {
      if (online) {
        pill.innerHTML = `<span class="pulse-dot"></span> <span>API ONLINE</span> <span style="opacity:0.6;margin-left:4px;">(<span id="active-visitors-count">1</span> active)</span>`;
      } else {
        pill.innerHTML = `<span class="pulse-dot" style="background:#ef4444;box-shadow:0 0 10px #ef4444;"></span> <span>RECONNECTING...</span>`;
      }
    }
  }
}

window.wsClient = new WebSocketClient();
window.addEventListener("DOMContentLoaded", () => {
  window.wsClient.connect();
});

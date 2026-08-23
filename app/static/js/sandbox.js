// Interactive FastAPI Sandbox Tester
const ENDPOINTS = [
  {
    name: "GET /api/analytics/overview (Platform Stats)",
    method: "GET",
    url: "/api/analytics/overview",
    body: null
  },
  {
    name: "GET /api/projects?featured_only=true (Featured Projects)",
    method: "GET",
    url: "/api/projects?featured_only=true",
    body: null
  },
  {
    name: "GET /api/skills/categorized (Grouped Tech Matrix)",
    method: "GET",
    url: "/api/skills/categorized",
    body: null
  },
  {
    name: "GET /api/experience (Career Timeline)",
    method: "GET",
    url: "/api/experience",
    body: null
  },
  {
    name: "GET /api/analytics/health (Uptime Probe)",
    method: "GET",
    url: "/api/analytics/health",
    body: null
  },
  {
    name: "GET /api/resume/json (Standard JSON Resume)",
    method: "GET",
    url: "/api/resume/json",
    body: null
  },
  {
    name: "POST /api/contact (Async BackgroundTask)",
    method: "POST",
    url: "/api/contact",
    body: JSON.stringify({
      name: "FastAPI Explorer",
      email: "recruiter@techventures.com",
      subject: "Interactive API Test",
      message: "Testing FastAPI BackgroundTasks and Pydantic validation live from sandbox!"
    }, null, 2)
  }
];

function initSandbox() {
  const selectEl = document.getElementById("sandbox-endpoint-select");
  const inputEl = document.getElementById("sandbox-url-input");
  const bodyEl = document.getElementById("sandbox-body-input");
  const executeBtn = document.getElementById("sandbox-execute-btn");
  const responseHeader = document.getElementById("sandbox-res-status");
  const responseTiming = document.getElementById("sandbox-res-time");
  const responseBody = document.getElementById("sandbox-res-body");

  if (!selectEl) return;

  // Populate endpoint options
  ENDPOINTS.forEach((ep, idx) => {
    const opt = document.createElement("option");
    opt.value = idx;
    opt.textContent = `${ep.method} ${ep.url}`;
    selectEl.appendChild(opt);
  });

  function updateFields() {
    const current = ENDPOINTS[selectEl.value];
    inputEl.value = current.url;
    if (current.method === "POST" && current.body) {
      bodyEl.style.display = "block";
      bodyEl.value = current.body;
    } else {
      bodyEl.style.display = "none";
    }
  }

  selectEl.addEventListener("change", updateFields);
  updateFields();

  executeBtn.addEventListener("click", async () => {
    const current = ENDPOINTS[selectEl.value];
    const url = inputEl.value;
    const method = current.method;
    
    responseBody.textContent = "⏳ Sending request to FastAPI backend...";
    responseHeader.textContent = "Status: Connecting...";
    responseTiming.textContent = "Latency: --";

    const startTime = performance.now();

    try {
      const options = {
        method: method,
        headers: {
          "Accept": "application/json"
        }
      };

      if (method === "POST") {
        options.headers["Content-Type"] = "application/json";
        options.body = bodyEl.value;
      }

      const res = await fetch(url, options);
      const endTime = performance.now();
      const elapsed = Math.round(endTime - startTime);
      const processTime = res.headers.get("X-Process-Time-Sec");

      responseHeader.textContent = `HTTP ${res.status} ${res.statusText}`;
      responseHeader.style.color = res.ok ? "#34d399" : "#f43f5e";
      responseTiming.textContent = `Roundtrip: ${elapsed}ms | Server: ${processTime ? (parseFloat(processTime)*1000).toFixed(1) + 'ms' : 'FastAPI'}`;

      const data = await res.json();
      responseBody.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      responseHeader.textContent = "Network Error";
      responseHeader.style.color = "#f43f5e";
      responseBody.textContent = `Error: ${err.message}`;
    }
  });
}

window.addEventListener("DOMContentLoaded", initSandbox);

// Main Application Logic
document.addEventListener("DOMContentLoaded", () => {
  fetchOverview();
  fetchSkills();
  fetchProjects();
  fetchExperience();
  setupContactForm();
  setupAdminModal();
});

// Toast notification helper
function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${type === "success" ? "✅" : "⚠️"}</span>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// 1. Fetch Overview & Stats
async function fetchOverview() {
  try {
    const res = await fetch("/api/analytics/overview");
    const json = await res.json();
    if (json.success && json.data) {
      const stats = json.data.stats;
      const dev = json.data.developer;

      const pCount = document.getElementById("stat-projects-count");
      if (pCount) pCount.textContent = stats.total_projects;

      const sCount = document.getElementById("stat-skills-count");
      if (sCount) sCount.textContent = stats.total_skills;

      const expCount = document.getElementById("stat-exp-count");
      if (expCount) expCount.textContent = stats.years_experience;

      const apisCount = document.getElementById("stat-apis-count");
      if (apisCount) apisCount.textContent = stats.apis_engineered;
    }
  } catch (err) {
    console.error("Error fetching overview:", err);
  }
}

// 2. Fetch & Render Skills Matrix
let allSkillsCategorized = [];
async function fetchSkills() {
  try {
    const res = await fetch("/api/skills/categorized");
    const json = await res.json();
    if (json.success && json.data) {
      allSkillsCategorized = json.data;
      renderSkillsTabs();
      renderSkills("All");
    }
  } catch (err) {
    console.error("Error loading skills:", err);
  }
}

function renderSkillsTabs() {
  const tabsContainer = document.getElementById("skills-tabs");
  if (!tabsContainer) return;

  tabsContainer.innerHTML = `<button class="tab-btn active" onclick="filterSkillsCategory('All', this)">All Technologies</button>`;
  allSkillsCategorized.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = "tab-btn";
    btn.textContent = cat.category;
    btn.onclick = () => filterSkillsCategory(cat.category, btn);
    tabsContainer.appendChild(btn);
  });
}

function filterSkillsCategory(category, btnEl) {
  document.querySelectorAll("#skills-tabs .tab-btn").forEach(b => b.classList.remove("active"));
  btnEl.classList.add("active");
  renderSkills(category);
}

function renderSkills(selectedCat) {
  const grid = document.getElementById("skills-grid");
  if (!grid) return;

  grid.innerHTML = "";
  let skillsToDisplay = [];

  if (selectedCat === "All") {
    allSkillsCategorized.forEach(c => {
      skillsToDisplay.push(...c.skills);
    });
  } else {
    const matched = allSkillsCategorized.find(c => c.category === selectedCat);
    if (matched) skillsToDisplay = matched.skills;
  }

  skillsToDisplay.forEach(s => {
    const card = document.createElement("div");
    card.className = "skill-card glass-panel";
    card.innerHTML = `
      <div class="skill-header">
        <div class="skill-icon-name">
          <span class="skill-icon">${s.icon}</span>
          <span class="skill-name">${s.name}</span>
        </div>
        <span class="skill-percent">${s.proficiency}%</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width: ${s.proficiency}%;"></div>
      </div>
      <div class="skill-footer">
        <span>${s.category}</span>
        <span>${s.experience_years}</span>
      </div>
    `;
    grid.appendChild(card);
  });
}

// 3. Fetch & Render Projects
let allProjects = [];
async function fetchProjects() {
  try {
    const res = await fetch("/api/projects?limit=50");
    const json = await res.json();
    if (json.success && json.items) {
      allProjects = json.items;
      renderProjects(allProjects);
      setupTechFilters();
    }
  } catch (err) {
    console.error("Error loading projects:", err);
  }
}

function setupTechFilters() {
  const filterContainer = document.getElementById("project-filters");
  if (!filterContainer) return;

  // Extract unique tech tags
  const tagsSet = new Set();
  allProjects.forEach(p => {
    p.tech_stack.forEach(t => tagsSet.add(t));
  });

  const popularTags = ["All", "FastAPI", "Python", "Docker", "PostgreSQL", "LangChain", "WebSockets"];
  filterContainer.innerHTML = "";

  popularTags.forEach(tag => {
    const btn = document.createElement("button");
    btn.className = `filter-btn ${tag === 'All' ? 'active' : ''}`;
    btn.textContent = tag;
    btn.onclick = () => {
      document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      if (tag === "All") {
        renderProjects(allProjects);
      } else {
        const filtered = allProjects.filter(p => p.tech_stack.some(t => t.toLowerCase() === tag.toLowerCase()));
        renderProjects(filtered);
      }
    };
    filterContainer.appendChild(btn);
  });
}

function renderProjects(projectsList) {
  const grid = document.getElementById("projects-grid");
  if (!grid) return;

  grid.innerHTML = "";
  if (projectsList.length === 0) {
    grid.innerHTML = `<p style="grid-column:1/-1;text-align:center;color:var(--text-dim);">No matching projects found.</p>`;
    return;
  }

  projectsList.forEach(p => {
    const tagsHtml = p.tech_stack.map(t => `<span class="tag-pill">${t}</span>`).join("");
    const card = document.createElement("div");
    card.className = "project-card glass-panel";
    card.innerHTML = `
      <div class="project-img-wrapper">
        <img class="project-img" src="${p.image_url || 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80'}" alt="${p.title}" loading="lazy">
        <span class="project-badge">${p.category}</span>
      </div>
      <div class="project-content">
        <h3 class="project-title">${p.title}</h3>
        <p class="project-summary">${p.summary}</p>
        <div class="project-tags">${tagsHtml}</div>
        <div class="project-actions">
          <button class="btn btn-outline btn-sm" onclick='showArchitectureModal(${JSON.stringify(p).replace(/'/g, "&apos;")})'>📐 Architecture</button>
          ${p.live_url ? `<a href="${p.live_url}" target="_blank" class="btn btn-primary btn-sm">⚡ Live Demo</a>` : ''}
          ${p.github_url ? `<a href="${p.github_url}" target="_blank" class="btn btn-outline btn-sm">⭐ GitHub</a>` : ''}
        </div>
      </div>
    `;
    grid.appendChild(card);
  });
}

// 4. Architecture Detail Modal
window.showArchitectureModal = function(project) {
  const modal = document.getElementById("arch-modal");
  const modalTitle = document.getElementById("arch-modal-title");
  const modalDesc = document.getElementById("arch-modal-desc");
  const modalNotes = document.getElementById("arch-modal-notes");
  const modalStack = document.getElementById("arch-modal-stack");

  if (!modal) return;
  modalTitle.textContent = project.title;
  modalDesc.textContent = project.description;
  modalNotes.textContent = project.architecture_notes || "Clean REST architecture with asynchronous lifecycle and type-safe contracts.";
  modalStack.innerHTML = project.tech_stack.map(t => `<span class="tag-pill" style="color:var(--accent-cyan);border-color:var(--accent-cyan);">${t}</span>`).join(" ");

  modal.classList.add("active");
};

// 5. Fetch & Render Career Timeline
async function fetchExperience() {
  try {
    const res = await fetch("/api/experience");
    const json = await res.json();
    if (json.success && json.data) {
      renderExperience(json.data);
    }
  } catch (err) {
    console.error("Error loading experience:", err);
  }
}

function renderExperience(items) {
  const timeline = document.getElementById("experience-timeline");
  if (!timeline) return;

  timeline.innerHTML = "";
  items.forEach(item => {
    const achievementsHtml = item.key_achievements.map(a => `<li>${a}</li>`).join("");
    const timelineItem = document.createElement("div");
    timelineItem.className = "timeline-item";
    timelineItem.innerHTML = `
      <div class="timeline-dot"></div>
      <div class="timeline-card glass-panel">
        <div class="timeline-header">
          <div>
            <div class="timeline-role">${item.role_or_degree}</div>
            <div class="timeline-org">${item.organization} &bull; <span style="font-size:0.85rem;color:var(--text-dim);">${item.location}</span></div>
          </div>
          <span class="timeline-period">${item.period}</span>
        </div>
        <p class="timeline-desc">${item.description}</p>
        <ul class="timeline-achievements">${achievementsHtml}</ul>
      </div>
    `;
    timeline.appendChild(timelineItem);
  });
}

// 6. Setup Contact Form with BackgroundTasks
function setupContactForm() {
  const form = document.getElementById("contact-form");
  const submitBtn = document.getElementById("contact-submit-btn");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("contact-name").value.trim();
    const email = document.getElementById("contact-email").value.trim();
    const subject = document.getElementById("contact-subject").value.trim();
    const message = document.getElementById("contact-message").value.trim();

    if (!name || !email || !message) {
      showToast("Please fill in all required fields", "error");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.innerHTML = "⏳ Sending & Triggering BackgroundTasks...";

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, subject, message })
      });

      const data = await res.json();
      if (res.ok && data.success) {
        showToast(data.message, "success");
        form.reset();
      } else {
        const errMsg = data.error?.message || "Failed to submit message";
        showToast(errMsg, "error");
      }
    } catch (err) {
      showToast(`Network Error: ${err.message}`, "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = "🚀 Send Message (Async Background Task)";
    }
  });
}

// 7. Setup Admin Modal & Management
let adminToken = localStorage.getItem("fastapi_portfolio_jwt");

function setupAdminModal() {
  const openBtn = document.getElementById("open-admin-btn");
  const modal = document.getElementById("admin-modal");
  const closeBtn = document.getElementById("close-admin-btn");
  const loginForm = document.getElementById("admin-login-form");
  const dashboardView = document.getElementById("admin-dashboard-view");
  const loginView = document.getElementById("admin-login-view");

  if (!modal) return;

  openBtn.addEventListener("click", () => {
    modal.classList.add("active");
    if (adminToken) {
      showAdminDashboard();
    } else {
      loginView.style.display = "block";
      dashboardView.style.display = "none";
    }
  });

  closeBtn.addEventListener("click", () => {
    modal.classList.remove("active");
  });

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const u = document.getElementById("admin-user").value;
    const p = document.getElementById("admin-pass").value;

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: u, password: p })
      });
      const data = await res.json();
      if (res.ok && data.access_token) {
        adminToken = data.access_token;
        localStorage.setItem("fastapi_portfolio_jwt", adminToken);
        showToast("Authenticated as Admin!", "success");
        showAdminDashboard();
      } else {
        showToast("Invalid admin credentials", "error");
      }
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  async function showAdminDashboard() {
    loginView.style.display = "none";
    dashboardView.style.display = "block";
    loadAdminInbox();
  }

  async function loadAdminInbox() {
    const listEl = document.getElementById("admin-inbox-list");
    if (!listEl) return;
    listEl.innerHTML = "<p>Loading messages...</p>";

    try {
      const res = await fetch("/api/contact/inbox", {
        headers: { "Authorization": `Bearer ${adminToken}` }
      });
      const data = await res.json();
      if (data.success && data.data) {
        if (data.data.length === 0) {
          listEl.innerHTML = "<p style='color:var(--text-dim);'>No messages received yet.</p>";
          return;
        }
        listEl.innerHTML = data.data.map(m => `
          <div style="background:rgba(255,255,255,0.03);border:1px solid var(--border-glass);padding:14px;border-radius:8px;margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
              <strong>${m.name} &lt;${m.email}&gt;</strong>
              <span style="font-size:0.8rem;color:var(--text-dim);">${new Date(m.created_at).toLocaleDateString()}</span>
            </div>
            <div style="color:var(--accent-cyan);font-size:0.85rem;margin-bottom:6px;">Subject: ${m.subject}</div>
            <p style="font-size:0.9rem;color:var(--text-muted);">${m.message}</p>
          </div>
        `).join("");
      }
    } catch (err) {
      listEl.innerHTML = `<p style='color:#ef4444;'>Failed to load inbox: ${err.message}</p>`;
    }
  }

  const logoutBtn = document.getElementById("admin-logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      adminToken = null;
      localStorage.removeItem("fastapi_portfolio_jwt");
      loginView.style.display = "block";
      dashboardView.style.display = "none";
      showToast("Logged out successfully");
    });
  }
}

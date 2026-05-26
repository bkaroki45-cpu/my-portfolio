// PARTICLE CANVAS
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let W, H, particles = [];

function resize() {
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

class Particle {
  constructor() { this.reset(); }
  reset() {
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.3;
    this.vy = (Math.random() - 0.5) * 0.3;
    this.r = Math.random() * 1.5 + 0.5;
    this.alpha = Math.random() * 0.5 + 0.1;
    this.color = Math.random() > 0.5 ? '59,130,246' : '168,85,247';
  }
  update() {
    this.x += this.vx; this.y += this.vy;
    if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${this.color},${this.alpha})`;
    ctx.fill();
  }
}

for (let i = 0; i < 100; i++) particles.push(new Particle());

function connectParticles() {
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const d = Math.sqrt(dx*dx + dy*dy);
      if (d < 120) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = `rgba(59,130,246,${0.08 * (1 - d/120)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, W, H);
  particles.forEach(p => { p.update(); p.draw(); });
  connectParticles();
  requestAnimationFrame(animate);
}
animate();

// CURSOR
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursor-ring');
let mx = 0, my = 0, rx = 0, ry = 0;
document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
function animCursor() {
  cursor.style.left = (mx - 6) + 'px';
  cursor.style.top = (my - 6) + 'px';
  rx += (mx - rx) * 0.12;
  ry += (my - ry) * 0.12;
  ring.style.left = (rx - 20) + 'px';
  ring.style.top = (ry - 20) + 'px';
  requestAnimationFrame(animCursor);
}
animCursor();
document.querySelectorAll('a,button,.skill-card,.project-card,.testimonial-card').forEach(el => {
  el.addEventListener('mouseenter', () => { cursor.style.transform = 'scale(2)'; ring.style.transform = 'scale(1.5)'; });
  el.addEventListener('mouseleave', () => { cursor.style.transform = 'scale(1)'; ring.style.transform = 'scale(1)'; });
});

// NAVBAR SCROLL
window.addEventListener('scroll', () => {
  document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
});

// FADE IN
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// DATA-DRIVEN PROJECT SHOWCASE
// Project cards are managed in the Django admin and injected into this page as JSON.
const projectDataEl = document.getElementById('project-data');
const projects = projectDataEl ? JSON.parse(projectDataEl.textContent) : [];

function createProjectVisual(project) {
  const accentMap = {
    fintech: ['92%', '74%', '58%'],
    civic: ['68%', '88%', '46%'],
    recruitment: ['82%', '52%', '70%'],
    education: ['62%', '78%', '56%'],
    calculator: ['48%', '64%', '86%'],
    default: ['70%', '62%', '54%']
  };
  const widths = accentMap[project.visual] || ['70%', '62%', '54%'];

  return `
    <div class="project-visual ${project.visual}">
      <div class="project-visual-bars">
        <span style="--w:${widths[0]}"></span>
        <span style="--w:${widths[1]}"></span>
        <span style="--w:${widths[2]}"></span>
      </div>
      <div class="project-visual-metric">
        <strong>${project.metric}</strong>
        <small>${project.visual.toUpperCase()} UI</small>
      </div>
    </div>
  `;
}

function createProjectCard(project, index) {
  const featureHtml = project.features.map(feature => `<span>${feature}</span>`).join('');
  const stackHtml = project.techStack.map(tech => `<span class="stack-pill">${tech}</span>`).join('');
  const highlightHtml = project.highlight ? `<div class="mpesa-badge">${project.highlight}</div>` : '';
  const liveClass = project.live ? 'project-link demo' : 'project-link demo disabled';
  const liveHref = project.live || '#projects';

  return `
    <article class="project-card fade-in is-showing ${project.featured ? 'featured-project' : ''}" style="transition-delay:${Math.min(index * 0.06, 0.3)}s" data-categories="${project.categories.join(',')}">
      <div class="project-thumb">
        <span class="project-status">${project.status}</span>
        <div class="project-thumb-inner">
          ${createProjectVisual(project)}
        </div>
      </div>
      <div class="project-body">
        ${highlightHtml}
        <h3 class="project-title">${project.title}</h3>
        <p class="project-desc">${project.description}</p>
        <div class="project-features">${featureHtml}</div>
        <div class="project-stack">${stackHtml}</div>
        <div class="project-links">
          <a href="${project.github}" class="project-link gh" target="_blank" rel="noopener">${project.githubLabel}</a>
          <a href="${liveHref}" class="${liveClass}" target="${project.live ? '_blank' : '_self'}" rel="noopener">${project.liveLabel}</a>
        </div>
      </div>
    </article>
  `;
}

function renderProjects(filter = 'All') {
  const gridEl = document.getElementById('projects-grid');
  if (!gridEl) return;

  const visibleProjects = projects.filter(project => project.categories.includes(filter));
  gridEl.innerHTML = visibleProjects.map(createProjectCard).join('');
  gridEl.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
}

function setupProjectFilters() {
  const filterButtons = document.querySelectorAll('.filter-chip');
  if (!filterButtons.length) return;

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      renderProjects(button.dataset.filter);
    });
  });
}

renderProjects();
setupProjectFilters();

document.addEventListener('mousemove', e => {
  const card = e.target.closest('.project-card');
  if (!card) return;
  const rect = card.getBoundingClientRect();
  card.style.setProperty('--mx', `${e.clientX - rect.left}px`);
  card.style.setProperty('--my', `${e.clientY - rect.top}px`);
});

document.addEventListener('mouseover', e => {
  if (!e.target.closest('.project-card')) return;
  cursor.style.transform = 'scale(2)';
  ring.style.transform = 'scale(1.5)';
});

document.addEventListener('mouseout', e => {
  if (!e.target.closest('.project-card')) return;
  cursor.style.transform = 'scale(1)';
  ring.style.transform = 'scale(1)';
});

// GITHUB CONTRIBUTION GRAPH
const grid = document.getElementById('gh-contribution-grid');
const levels = [0,0,0,1,1,2,3,2,1,0,0,1,2,3,4,3,2,1,0,0,1,1,2,2,3,3,2,1,0,0,0,1,2,3,4,3,2,1,0,0,1,2,3,4,4,3,2,1,0,1,1,2,3,3,2,1,0,0,1,2,3,4,3,2,1,0];
const weeks = 52;
if (grid) {
  grid.innerHTML = '';
  for (let w = 0; w < weeks; w++) {
    const col = document.createElement('div');
    col.style.cssText = 'display:flex;flex-direction:column;gap:3px';
    for (let d = 0; d < 7; d++) {
      const cell = document.createElement('div');
      cell.style.cssText = 'width:14px;height:14px;border-radius:3px;transition:transform .2s ease, box-shadow .2s ease';
      const lvl = levels[(w * 7 + d) % levels.length] + (Math.random() > 0.7 ? 1 : 0);
      const clamped = Math.min(lvl, 4);
      const colors = ['rgba(255,255,255,0.05)','rgba(59,130,246,0.2)','rgba(59,130,246,0.45)','rgba(59,130,246,0.7)','#3b82f6'];
      cell.style.background = colors[clamped];
      if (clamped === 4) cell.style.boxShadow = '0 0 6px rgba(59,130,246,0.5)';
      col.appendChild(cell);
    }
    grid.appendChild(col);
  }
}

// TYPEWRITER HERO
const words = ['Scalable Web Systems', 'Powerful APIs', 'Impactful Solutions', 'Fintech Integrations'];
let wi = 0, ci = 0, deleting = false;
const heroTitle = document.querySelector('.hero-title .grad-text');
if (heroTitle) {
  function type() {
    const word = words[wi];
    if (!deleting) {
      heroTitle.textContent = word.substring(0, ci++);
      if (ci > word.length) { deleting = true; setTimeout(type, 1800); return; }
    } else {
      heroTitle.textContent = word.substring(0, ci--);
      if (ci < 0) { deleting = false; wi = (wi + 1) % words.length; ci = 0; }
    }
    setTimeout(type, deleting ? 40 : 80);
  }
  setTimeout(type, 1500);
}

// COUNTER ANIMATION
function animateCounter(el, target) {
  let current = 0;
  const suffix = el.dataset.suffix || '';
  const inc = target / 60;
  const timer = setInterval(() => {
    current = Math.min(current + inc, target);
    el.textContent = Math.floor(current) + suffix;
    if (current >= target) clearInterval(timer);
  }, 20);
}
const statNums = document.querySelectorAll('.stat-num');
const statObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const text = e.target.textContent;
      const num = parseInt(text);
      animateCounter(e.target, num);
      statObs.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
statNums.forEach(el => statObs.observe(el));

// CONTACT CTA LOADING STATE
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', () => {
    const button = contactForm.querySelector('.btn-submit');
    if (!button) return;
    button.classList.add('is-loading');
    button.lastChild.textContent = ' Sending...';
  });
}

/**
 * Particles Animation System
 * Math-based particle effects for hero sections
 */

class ParticleSystem {
  constructor(containerId, particleCount = 50) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;
    
    this.particleCount = particleCount;
    this.particles = [];
    this.init();
  }

  init() {
    // Create particles container
    const particlesDiv = document.createElement('div');
    particlesDiv.className = 'particles';
    this.container.appendChild(particlesDiv);

    // Generate particles with mathematical distribution
    for (let i = 0; i < this.particleCount; i++) {
      this.createParticle(particlesDiv);
    }
  }

  createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';

    // Mathematical random positioning
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const size = Math.random() * 4 + 2; // 2-6px
    const duration = Math.random() * 4 + 3; // 3-7s animation

    particle.style.left = x + '%';
    particle.style.top = y + '%';
    particle.style.width = size + 'px';
    particle.style.height = size + 'px';
    particle.style.setProperty('--particle-duration', duration + 's');

    container.appendChild(particle);
  }
}

/**
 * Animated Counter
 * Counts up to a target number with easing
 */
class AnimatedCounter {
  constructor(element, target, duration = 2000) {
    this.element = element;
    this.target = target;
    this.duration = duration;
    this.current = 0;
    this.animate();
  }

  animate() {
    const start = Date.now();
    const animate = () => {
      const progress = Math.min((Date.now() - start) / this.duration, 1);
      
      // Easing: easeOutCubic
      const eased = 1 - Math.pow(1 - progress, 3);
      this.current = Math.floor(eased * this.target);
      
      this.element.textContent = this.current.toLocaleString();
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };
    
    requestAnimationFrame(animate);
  }
}

/**
 * Form Input Animation
 * Adds focus effects and validation states
 */
class FormAnimation {
  constructor(formSelector) {
    this.form = document.querySelector(formSelector);
    if (!this.form) return;

    this.inputs = this.form.querySelectorAll('input, textarea, select');
    this.init();
  }

  init() {
    this.inputs.forEach(input => {
      // Focus effect
      input.addEventListener('focus', () => {
        input.parentElement.style.boxShadow = 
          '0 0 0 3px rgba(102, 126, 234, 0.1)';
      });

      // Blur effect
      input.addEventListener('blur', () => {
        input.parentElement.style.boxShadow = 'none';
      });

      // Validation feedback
      input.addEventListener('change', () => {
        if (input.checkValidity && !input.checkValidity()) {
          input.style.borderColor = 'var(--danger)';
        } else if (input.value) {
          input.style.borderColor = 'var(--success)';
        }
      });
    });
  }
}

/**
 * Smooth Scroll Animation
 */
function smoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

/**
 * Intersection Observer for reveal animations
 */
function observeElements() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.card, .stat-card, .alert').forEach(el => {
    observer.observe(el);
  });
}

/**
 * Navbar scroll effect
 */
function navbarScrollEffect() {
  const navbar = document.querySelector('.navbar');
  if (!navbar) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      navbar.style.boxShadow = 'var(--shadow-lg)';
    } else {
      navbar.style.boxShadow = 'var(--shadow-md)';
    }
  });
}

/**
 * Initialize all animations when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  // Initialize particle system for hero
  new ParticleSystem('hero-particles');

  // Initialize form animations
  new FormAnimation('form');

  // Smooth scroll
  smoothScroll();

  // Observe elements for reveal animations
  observeElements();

  // Navbar effects
  navbarScrollEffect();

  // Animate counters if they exist
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.getAttribute('data-count'));
    new AnimatedCounter(el, target);
  });
});

// Export for modular use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { ParticleSystem, AnimatedCounter, FormAnimation };
}

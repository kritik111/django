window.addEventListener('DOMContentLoaded', () => {
  // Animate stem growth
  const stem = document.getElementById('stem');
  setTimeout(() => {
    stem.style.transform = 'scaleY(1)';
    stem.classList.add('sway');
  }, 300);

  // Animate leaves sprouting
  const leafLeft = document.getElementById('leaf-left');
  const leafRight = document.getElementById('leaf-right');
  setTimeout(() => {
    leafLeft.style.opacity = 1;
    leafLeft.style.transform = 'scale(1.1)';
    leafRight.style.opacity = 1;
    leafRight.style.transform = 'scale(1.1)';
  }, 1200);

  // Animate petals unfolding
  const petals = document.querySelectorAll('.petal');
  setTimeout(() => {
    petals.forEach((petal, i) => {
      setTimeout(() => {
        petal.setAttribute('rx', '40');
        petal.setAttribute('ry', '80');
      }, i * 120);
    });
  }, 1800);

  // Animate flower center
  const center = document.getElementById('flower-center');
  setTimeout(() => {
    center.setAttribute('r', '28');
  }, 3000);

  // Sway the whole flower
  const stemGroup = document.getElementById('stem-group');
  setTimeout(() => {
    stemGroup.classList.add('sway');
  }, 2000);

  // Animate sun glowing and moving
  const sun = document.getElementById('sun');
  let sunAngle = 0;
  function animateSun() {
    sunAngle += 0.003;
    const cx = 320 + Math.sin(sunAngle) * 60;
    const cy = 100 + Math.cos(sunAngle) * 20;
    sun.setAttribute('cx', cx);
    sun.setAttribute('cy', cy);
    // Make flower follow the sun
    const flowerGroup = document.getElementById('petals-group');
    const swayAmount = Math.sin(sunAngle) * 8;
    flowerGroup.setAttribute('transform', `rotate(${swayAmount} 200 400)`);
    requestAnimationFrame(animateSun);
  }
  animateSun();
});
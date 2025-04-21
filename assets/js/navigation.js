// Navigation functionality for module content
document.addEventListener('DOMContentLoaded', function() {
  const unitCards = document.querySelectorAll('.unit-card');
  const navLinks = document.querySelectorAll('.nav-link');
  const navContent = document.querySelector('.module-nav-content');
  
  // Highlight active nav item based on scroll position
  function updateActiveNavItem() {
    let currentActiveIndex = 0;
    
    unitCards.forEach((card, index) => {
      const rect = card.getBoundingClientRect();
      if (rect.top <= 150 && rect.bottom >= 150) {
        currentActiveIndex = index;
      }
    });
    
    navLinks.forEach((link, index) => {
      if (index === currentActiveIndex) {
        link.classList.add('active');
        // Scroll nav to keep active item visible
        if (navContent) {
          const linkOffset = link.offsetTop;
          const navHeight = navContent.clientHeight;
          const scrollTop = navContent.scrollTop;
          
          if (linkOffset < scrollTop || linkOffset > scrollTop + navHeight) {
            navContent.scrollTop = linkOffset - (navHeight / 2);
          }
        }
      } else {
        link.classList.remove('active');
      }
    });
  }
  
  // Handle click on nav items
  navLinks.forEach((link, index) => {
    link.addEventListener('click', function(e) {
      // Highlight clicked nav item
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');
      
      // Keep the nav scroll position
      setTimeout(() => {
        if (navContent) {
          const linkOffset = link.offsetTop;
          const navHeight = navContent.clientHeight;
          navContent.scrollTop = linkOffset - (navHeight / 2);
        }
      }, 100);
    });
  });
  
  // Update active nav item on scroll
  window.addEventListener('scroll', updateActiveNavItem);
  
  // Initial update
  updateActiveNavItem();
}); 
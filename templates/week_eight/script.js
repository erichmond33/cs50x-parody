const navSlide = () => {
  const burger = document.querySelector('.burger');
  const nav = document.querySelector('.nav-links');
  const navLinks = document.querySelectorAll('.nav-links li');

  burger.addEventListener('click', () => {
    //Toggle Nav
    nav.classList.toggle('nav-active');


    //Animate Links
    navLinks.forEach((link, index) => {
      console.log(index / 7);
      link.style.animation = 'navLinkFade 1s ease forwards 1s';
    });
    //Burger animation
    burger.classList.toggle('toggle');
  });
}

navSlide();


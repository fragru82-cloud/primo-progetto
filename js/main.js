// =============================================
// GLOBALINK SECURITY - JavaScript Principale
// =============================================

document.addEventListener('DOMContentLoaded', function () {

    // --- Header scroll effect ---
    const header = document.getElementById('header');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            header.classList.add('header--scrolled');
        } else {
            header.classList.remove('header--scrolled');
        }
    });

    // --- Mobile menu toggle ---
    const hamburger = document.getElementById('hamburger');
    const nav = document.getElementById('nav');

    hamburger.addEventListener('click', function () {
        nav.classList.toggle('nav--open');
        // Animate hamburger
        this.classList.toggle('active');
    });

    // Chiudi menu al click su un link
    document.querySelectorAll('.nav__link').forEach(function (link) {
        link.addEventListener('click', function () {
            nav.classList.remove('nav--open');
            hamburger.classList.remove('active');
        });
    });

    // --- Form submission ---
    var contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            var nome = document.getElementById('nome').value.trim();
            var telefono = document.getElementById('telefono').value.trim();
            var servizio = document.getElementById('servizio').value;

            if (!nome || !telefono || !servizio) {
                alert('Per favore compila tutti i campi.');
                return;
            }

            // Componi messaggio WhatsApp
            var messaggio = 'Ciao, sono ' + nome + '. '
                + 'Sono interessato al servizio: ' + servizio + '. '
                + 'Il mio numero è: ' + telefono + '. '
                + 'Potete ricontattarmi?';

            var whatsappUrl = 'https://wa.me/393801448789?text=' + encodeURIComponent(messaggio);
            window.open(whatsappUrl, '_blank');

            // Reset form
            contactForm.reset();
        });
    }

    // --- Smooth scroll per link interni ---
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                var offset = header.offsetHeight + 16;
                var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });

});

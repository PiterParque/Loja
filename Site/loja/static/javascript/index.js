const slides = document.querySelectorAll('.carrosel-item');
const btnProximo = document.querySelector('.proximo');
const btnAnterior = document.querySelector('.anterior');

let indiceAtual = 0;

function mostrarSlide(indice) {
    slides.forEach(slide => slide.classList.remove('ativo'));
    slides[indice].classList.add('ativo');
}

btnProximo.addEventListener('click', () => {
    indiceAtual = (indiceAtual + 1) % slides.length;
    mostrarSlide(indiceAtual);
});

btnAnterior.addEventListener('click', () => {
    indiceAtual = (indiceAtual - 1 + slides.length) % slides.length;
    mostrarSlide(indiceAtual);
});

// Inicia mostrando o primeiro
mostrarSlide(indiceAtual);

// Troca automática a cada 5 segundos
setInterval(() => {
    indiceAtual = (indiceAtual + 1) % slides.length;
    mostrarSlide(indiceAtual);
}, 5000);

document.addEventListener("DOMContentLoaded", function() {
    // Assume que qualquer carregamento de página deve mostrar o loader,
    // exceto quando sabemos que é uma navegação de volta pelo histórico.
    if (!sessionStorage.getItem('navigated')) {
        document.getElementById("loading-screen").style.display = "flex";
        // Espera um curto período antes de ocultar para garantir que seja visível
        setTimeout(() => {
            document.getElementById("loading-screen").style.display = "none";
        }, 100); // Ajuste esse tempo conforme necessário
    }

    document.querySelectorAll('a').forEach(function(link) {
        link.addEventListener('click', function(e) {
            sessionStorage.setItem('navigated', 'true');
            document.getElementById("loading-screen").style.display = "flex";
        });
    });

    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function() {
            sessionStorage.setItem('navigated', 'true');
            document.getElementById("loading-screen").style.display = "flex";
        });
    });
});

window.addEventListener('pageshow', function(event) {
    if (event.persisted || sessionStorage.getItem('navigated') === 'true') {
        document.getElementById("loading-screen").style.display = "none";
        sessionStorage.removeItem('navigated');
    }
});

window.addEventListener('beforeunload', function() {
    // Isso força a exibição do loader antes da página começar a descarregar,
    // incluindo recarregamentos via F5 ou comando de recarga do navegador.
    document.getElementById("loading-screen").style.display = "flex";
});

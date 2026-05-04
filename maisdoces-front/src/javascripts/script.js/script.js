// O QUE FAZ: inicia os comportamentos da página quando o DOM termina de carregar.
// ONDE APARECE: lógica global da navegação.
// QUANDO ATUA: no carregamento da página.
$(document).ready(function() {
    // Quando clicar em qualquer link do menu desktop
    $('#nav_list .nav-item').on('click', function() {
        // 1. Remove a classe 'active' de TODOS os itens do menu
        $('#nav_list .nav-item').removeClass('active');      
        // 2. Adiciona a classe 'active' apenas no item que recebeu o clique
        $(this).addClass('active');
    });
});
    
// O QUE FAZ: abre/fecha menu mobile e alterna ícone do botão.
// ONDE APARECE: botão #mobile_btn e bloco #mobile_menu.
// QUANDO ATUA: ao clicar no botão hambúrguer.
$('#mobile_btn').on('click', function () {
    $('#mobile_menu').toggleClass('active');
    $('#mobile_btn').find('i').toggleClass('fa-x');
});

// O QUE FAZ: controla o item ativo da navegação baseado na rolagem da página.
// ONDE APARECE: navegação desktop e mobile.
// QUANDO ATUA: ao rolar a página.
$(window).on('scroll', function () {
    // Pega a altura do header no momento exato
    const headerHeight = $('header').outerHeight(); 
    const scrollPos = $(window).scrollTop() + headerHeight + 20; // 20px de margem

    $('section').each(function () {
        const sectionTop = $(this).offset().top;
        const sectionBottom = sectionTop + $(this).outerHeight();
        const id = $(this).attr('id');

        // Se a rolagem estiver dentro da área da seção
        if (scrollPos >= sectionTop && scrollPos < sectionBottom) {
            $('.nav-item').removeClass('active');
            $(`.nav-item a[href="#${id}"]`).parent().addClass('active');
        }
    });
});
    
// O QUE FAZ: inicializa a biblioteca ScrollReveal para animações ao rolar.
// ONDE APARECE: elementos da página.
// QUANDO ATUA: após o carregamento da página.
const sr = ScrollReveal({
    origin: 'top', // Origem da animação (de cima)
    distance: '50px', // Distância da animação
    duration: 2000, // Duração da animação em milissegundos
    reset: true // Reinicia a animação ao sair da viewport
});

// O QUE FAZ: aplica o efeito de revelação nos elementos.
// ONDE APARECE: elementos específicos da página.
// QUANDO ATUA: quando os elementos entram na viewport.
sr.reveal('.title', { delay: 200 }); // Título com delay de 200ms
sr.reveal('.description', { delay: 400 }); // Descrição com delay de 400ms
sr.reveal('.btn-default', { delay: 600 }); // Botões com delay de 600ms
sr.reveal('.hero-cake-image', { origin: 'right', delay: 400 }); // Imagem do bolo vindo da direita

// O QUE FAZ: atualiza item ativo da navegação e fecha menu mobile.
// ONDE APARECE: links da navbar desktop e mobile.
// QUANDO ATUA: ao clicar em qualquer link de navegação.
$('#nav_list .nav-item a, #mobile_nav_list .nav-item a').on('click', function () {
    const alvo = $(this).attr('href');

    // Remove a classe 'active' de todos os itens
    $('#nav_list .nav-item, #mobile_nav_list .nav-item').removeClass('active');
    
    // Adiciona a classe 'active' ao item clicado
    $(`#nav_list .nav-item a[href="${alvo}"]`).parent().addClass('active');
    $(`#mobile_nav_list .nav-item a[href="${alvo}"]`).parent().addClass('active');

    // Fecha o menu mobile
    $('#mobile_menu').removeClass('active');
});

// O QUE FAZ: adiciona efeito de encolhimento ao header ao rolar a página.
// ONDE APARECE: header da página.
// QUANDO ATUA: ao rolar a página.
$(window).on('scroll', function() {
    if ($(window).scrollTop() > 50) {
        $('header').addClass('shrink'); // Adiciona classe para header menor
    } else {
        $('header').removeClass('shrink'); // Remove classe para header normal
    }
});

// O QUE FAZ: carrega produtos da API e renderiza no cardápio
// ONDE APARECE: seção #menu
// QUANDO ATUA: após o DOM carregar
async function loadProducts() {
    try {
        // Faz requisição para a API de produtos
        const response = await fetch('http://localhost:8000/api/products');
        const products = await response.json();
        renderProducts(products); // Renderiza os produtos na página
    } catch (error) {
        console.error('Erro ao carregar produtos:', error);
        // Exibe mensagem de erro amigável ao usuário
        $('#dishes').html('<p style="text-align: center; color: #666; padding: 20px;">Erro ao carregar produtos. Por favor, tente novamente mais tarde.</p>');
    }
}

// O QUE FAZ: renderiza os produtos no cardápio
// ONDE APARECE: container #dishes
// QUANDO ATUA: quando os produtos são carregados da API
function renderProducts(products) {
    const dishesContainer = $('#dishes');
    dishesContainer.empty(); // Limpa o container antes de renderizar

    // Verifica se há produtos disponíveis
    if (products.length === 0) {
        dishesContainer.html('<p style="text-align: center; color: #666; padding: 20px;">Nenhum produto disponível no momento.</p>');
        return;
    }

    // Renderiza cada produto
    products.forEach(product => {
        // Cria string de estrelas baseada na avaliação
        const stars = '★'.repeat(product.rating) + '☆'.repeat(5 - product.rating);
        
        // Cria HTML do card do produto
        const productHtml = `
            <article class="dish">
                <!-- Selo de favorito -->
                <div class="dish-heart">
                    <i class="fa-solid fa-heart"></i>
                </div>
                
                <!-- Imagem do produto -->
                <img src="${product.image}" class="dish-image ${product.image_class || 'dish-image-donuts'}" alt="${product.title}">
                
                <!-- Título do produto -->
                <h3 class="dish-title">${product.title}</h3>
                
                <!-- Descrição do produto -->
                <span class="dish-description">${product.description}</span>
                
                <!-- Avaliação do produto -->
                <div class="dish-rate">
                    <span>${stars}</span>
                    <span>(${product.rating_count}+)</span>
                </div>
                
                <!-- Preço e botão de ação -->
                <div class="dish-price">
                    <h4>${product.price}</h4>
                    <button class="btn-default btn-icon" type="button" aria-label="Adicionar ${product.title} ao carrinho">
                        <i class="fa-solid fa-basket-shopping"></i>
                    </button>
                </div>
            </article>
        `;
        
        // Adiciona o card ao container
        dishesContainer.append(productHtml);
    });
}

// Carrega produtos quando o DOM estiver pronto
$(document).ready(function() {
    loadProducts();
});

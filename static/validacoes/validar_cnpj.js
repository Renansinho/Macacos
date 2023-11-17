function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]+/g, ''); // Remove caracteres não numéricos

    if (cnpj.length !== 14) {
        return false; // CNPJ deve ter 14 dígitos
    }

    // Verifica se todos os dígitos são iguais, o que é inválido
    if (/^(\d)\1+$/.test(cnpj)) {
        return false;
    }

    // Calcula os dígitos verificadores
    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }

    let resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);

    if (resultado !== parseInt(digitos.charAt(0))) {
        return false;
    }

    tamanho += 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += numeros.charAt(tamanho - i) * pos--;
        if (pos < 2) {
            pos = 9;
        }
    }

    resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);

    return resultado === parseInt(digitos.charAt(1));
}

// Função para executar a validação do CNPJ antes de enviar o formulário
function validarFormulario() {
    const cnpjInput = document.getElementById('cpf_cnpj'); // Corrigido o ID aqui
    const cnpj = cnpjInput.value;

    if (!validarCNPJ(cnpj)) {
        alert('CNPJ inválido!');
        cnpjInput.focus();
        return false;
    }

    return true;
}

// Adicione um ouvinte de evento para o formulário
document.getElementById('cnpj-valida').addEventListener('submit', function (event) {
    if (!validarFormulario()) {
        event.preventDefault(); // Impede o envio do formulário se o CNPJ for inválido
    }
});

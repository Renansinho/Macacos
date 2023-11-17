function mascara_tel(event) {
    var tel_esta = document.getElementById("tel_empresa");
    var input = event.target;

    // Remove caracteres não numéricos
    var numericValue = input.value.replace(/\D/g, "");

    if (numericValue.length <= 14) {
        // Adiciona os caracteres da máscara
        var formattedValue = '';
        for (var i = 0; i < numericValue.length; i++) {
            if (i === 0) formattedValue += '(';
            else if (i === 2) formattedValue += ')';
            else if (i === 8) formattedValue += '-';
            formattedValue += numericValue.charAt(i);
        }
        tel_esta.value = formattedValue;
    } else {
        // Caso o usuário digite mais do que 14 caracteres, remova os extras
        tel_esta.value = numericValue.substring(0, 14);
    }
}

var telInput = document.getElementById("tel_empresa");
telInput.addEventListener("input", mascara_tel);

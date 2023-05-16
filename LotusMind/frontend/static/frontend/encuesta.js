function seleccionarOpcion(elemento) {
    // Elimina la clase 'selected' de todos los botones
    const botones = document.querySelectorAll('.button');
    botones.forEach(boton => {
        boton.classList.remove('selected');
    });

    // Agrega la clase 'selected' al botón seleccionado
    elemento.classList.add('selected');

    // Guarda el valor de la respuesta seleccionada
    respuestaSeleccionada = elemento.value;
}
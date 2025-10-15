#include <stdio.h>

int main() {
    FILE *archivo;           // Puntero al archivo
    char caracter;           // Variable para leer carácter por carácter

    archivo = fopen("capturas.txt", "r");  // Abre el archivo en modo lectura

    if (archivo == NULL) {              // Verifica si se pudo abrir
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }

    printf("Contenido del archivo:\n");

    // Lee e imprime cada carácter hasta el final del archivo (EOF)
    while ((caracter = fgetc(archivo)) != EOF) {
        printf("%c", caracter);
    }

    fclose(archivo); // Cierra el archivo
    return 0;
}

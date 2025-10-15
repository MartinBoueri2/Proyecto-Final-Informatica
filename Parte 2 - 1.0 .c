#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CAPTURAS 1000
#define MAX_LINEA    256

typedef struct {
    int   numero;
    double temperatura;
    char  tendencia[8]; 
    char  fecha[32];
} Captura;

int main(void) {
    FILE *archivo = fopen("capturas.txt", "r");
    if (!archivo) {
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }

    Captura capturas[MAX_CAPTURAS];
    int n = 0;

    char linea[MAX_LINEA];

    while (n < MAX_CAPTURAS && fgets(linea, sizeof(linea), archivo)) {
        linea[strcspn(linea, "\r\n")] = '\0';

        int numero;
        double temp;
        char tendencia[8];
        char fecha[32];

        int ok = sscanf(linea,
                        "Captura %d: %lf%*[^,], Tendencia: %7[^,], Fecha: %31[^\n]",
                        &numero, &temp, tendencia, fecha);

        if (ok == 4) {
            capturas[n].numero      = numero;
            capturas[n].temperatura = temp;
            strncpy(capturas[n].tendencia, tendencia, sizeof(capturas[n].tendencia) - 1);
            capturas[n].tendencia[sizeof(capturas[n].tendencia) - 1] = '\0';

            strncpy(capturas[n].fecha, fecha, sizeof(capturas[n].fecha) - 1);
            capturas[n].fecha[sizeof(capturas[n].fecha) - 1] = '\0';

            n++;
        }
    }

    fclose(archivo);

    // Muestra lecturas
    printf("Leidas %d capturas:\n", n);
    for (int i = 0; i < n; i++) {
        printf("Captura %d: %.2f°C, Tendencia: %s, Fecha: %s\n",
               capturas[i].numero,
               capturas[i].temperatura,
               capturas[i].tendencia,
               capturas[i].fecha);
    }

    return 0;
}

#### RESPUESTAS PRUEBA TECNICA BTG ###

1. Indique con sus propias palabras, qué tecnologías utilizaría para garantizar la
solución. Justifique su respuesta.

Las tecnologías que utilizaría para la solución son las siguientes:

Backend:

    Lenguaje: Python
        Framework: FastAPI
            Razones:
            Es un framework moderno y de alto rendimiento.
            Soporta tipado estático con Pydantic, lo que mejora la seguridad y el manejo de errores.
            Excelente documentación y fácil de usar para la creación de APIs RESTful.

        Base de Datos: PostgreSQL
            Razones:
            Es robusta y escalable.
            Soporta transacciones y operaciones complejas.
            Buena integración con Python a través de bibliotecas como SQLAlchemy o asyncpg.

        ORM (Object-Relational Mapping): SQLAlchemy
            Razones:
            Facilita las operaciones CRUD.
            Permite un manejo de la base de datos más limpio y con menos errores.

    Mensajería/Notificaciones:
        Email: SMTP (Simple Mail Transfer Protocol)
        Bibliotecas: smtplib o servicios externos como SendGrid.
        SMS: Servicios externos como Twilio.
            Razones:
            Ofrecen APIs fáciles de usar.
            Fiabilidad y escalabilidad.

Frontend:

    Lenguaje: JavaScript
        Framework/Biblioteca: React
            Razones:
            Es una biblioteca popular y bien soportada para la creación de interfaces de usuario dinámicas.
            Gran ecosistema y comunidad de soporte.
            Fácil integración con bibliotecas de estado como Redux o Context API para el manejo del estado global.

    Estilos:
        CSS: con herramientas como SASS o Styled-components.
        Biblioteca de componentes: Material-UI o Ant Design
            Razones:
            Ofrecen componentes predefinidos y personalizables que aceleran el desarrollo.
            Diseño responsivo y estéticamente agradable.

Infraestructura:

    Despliegue en la Nube:
        Proveedor: AWS (Amazon Web Services), Azure, o Google Cloud Platform (GCP)
            Razones:
            Ofrecen servicios gestionados para bases de datos, cómputo, y mensajería.
            Escalabilidad y alta disponibilidad.
            Herramientas de monitoreo y seguridad robustas.

        Docker: para contenerización y fácil despliegue en cualquier entorno.
            Razones:
            Asegura consistencia entre entornos de desarrollo, prueba y producción.
            Facilita la gestión de dependencias y el escalado.
            Seguridad y Calidad:
            Manejo de Excepciones: Implementar manejo de excepciones detallado en ambos frontend y backend para asegurar que los errores se manejen adecuadamente y se proporcionen mensajes útiles a los usuarios.

    Pruebas Unitarias y de Integración:
        Backend: pytest, unittest
        Frontend: Jest, React Testing Library
            Razones:
            Aseguran que cada componente de la aplicación funcione correctamente de manera individual y en conjunto.
            CI/CD: Herramientas como GitHub Actions o GitLab CI para automatizar pruebas y despliegues.
            Monitoreo y Logs: Implementar herramientas de monitoreo y logging para detectar y diagnosticar problemas en producción.
            Ejemplos: Prometheus, Grafana, ELK stack (Elasticsearch, Logstash, Kibana).

2. Diseñe un modelo de datos NoSQL que permita la solución al problema.

* Colección de Clientes ('clients'):

    {
      "_id": "ObjectId('60c72b2f9af1f2d3b4b8d3e1')",
      "name": "Juan Perez",
      "email": "juan.perez@gmail.com",
      "phone": "+1234567890",
      "balance": 425000,
      "subscriptions": [
        {
          "fund_id": 1,
          "fund_name": "FPV_BTG_PACTUAL_RECAUDADORA",
          "amount": 75000,
          "date_subscribed": "2024-07-01T10:00:00Z",
          "transaction_id": "txn_001"
        }
      ],
      "transaction_history": [
        {
          "transaction_id": "txn_001",
          "fund_id": 1,
          "fund_name": "FPV_BTG_PACTUAL_RECAUDADORA",
          "amount": 75000,
          "type": "subscription",
          "date": "2024-07-01T10:00:00Z"
        }
      ],
      "notification_preference": "email"
    }
* Colección de Fondos ('funds')

    {
      "_id": "ObjectId('60c72b2f9af1f2d3b4b8d3e2')",
      "fund_id": 1,
      "name": "FPV_BTG_PACTUAL_RECAUDADORA",
      "min_amount": 75000,
      "category": "FPV"
    }
* Colección de Transacciones ('transactions')

    {
      "_id": "ObjectId('60c72b2f9af1f2d3b4b8d3e3')",
      "transaction_id": "txn_001",
      "client_id": "ObjectId('60c72b2f9af1f2d3b4b8d3e1')",
      "fund_id": 1,
      "fund_name": "FPV_BTG_PACTUAL_RECAUDADORA",
      "amount": 75000,
      "type": "subscription", // or "cancellation"
      "date": "2024-07-01T10:00:00Z"
    }

### DESCRIPCIÓN DEL MODELO DE DATOS ###

1. Clientes (clients):

* Cada documento representa un cliente.
* Almacena la información personal del cliente, incluyendo el saldo actual.
* Incluye una lista de suscripciones activas (subscriptions), donde cada suscripción tiene el ID del fondo, nombre, monto suscrito, fecha de suscripción y un ID de transacción.
* Almacena un historial de transacciones (transaction_history), donde cada transacción tiene el ID del fondo, nombre, monto, tipo (suscripción o cancelación), fecha y un ID de transacción.
* Contiene una preferencia de notificación (notification_preference), que puede ser "email", "sms" u otra.

2. Fondos (funds):

* Cada documento representa un fondo de inversión disponible para suscripción.
* Almacena el ID del fondo, nombre, monto mínimo de vinculación y categoría.

3. Transacciones (transactions):

* Cada documento representa una transacción realizada por un cliente.
* Almacena el ID de la transacción, ID del cliente, ID del fondo, nombre del fondo, monto, tipo de transacción (suscripción o cancelación) y fecha.

Parte 2

1. Obtener los nombres de los clientes los cuales tienen inscrito algún producto disponible sólo en las sucursales que visitan.

USE BTG;

SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
JOIN Inscripción i ON c.id = i.idCliente
JOIN Disponibilidad d ON i.idProducto = d.idProducto
JOIN Visitan v ON c.id = v.idCliente AND d.idSucursal = v.idSucursal
WHERE NOT EXISTS (
    SELECT 1
    FROM Disponibilidad d2
    WHERE d2.idProducto = i.idProducto
    AND d2.idSucursal NOT IN (
        SELECT v2.idSucursal
        FROM Visitan v2
        WHERE v2.idCliente = c.id
    )
);


CREATE DATABASE productos;

use productos;

create table producto (
ProductId int AUTO_INCREMENT primary key,
Nombre varchar(255) not null,
descripcion text,
price decimal(10,2) not null,
cantidad int not null
);

CREATE TABLE InventoryTransactions (
TransactionID INT AUTO_INCREMENT  PRIMARY KEY,
ProductID INT,
PreviousQuantity INT,
NewQuantity INT,
TransactionDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
TransactionType ENUM('Entrada', 'Salida') NOT NULL,
FOREIGN KEY (ProductID) REFERENCES producto(ProductId)
);

INSERT INTO producto (nombre, descripcion, price, cantidad) values 
('Jabón', 'Articulo de limpieza', 8.00, 10),
('Bola', 'juguete de esfera', 50.00, 25);




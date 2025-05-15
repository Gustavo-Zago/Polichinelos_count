CREATE DATABASE feira;
USE feira;

CREATE TABLE Usuarios (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    insta VARCHAR(100)
);

CREATE TABLE polichinelo (
    idpol INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    idusuario INT,
    contpol INT,
    FOREIGN KEY (idusuario) REFERENCES Usuarios(id)
);

#drop database feira
SELECT * FROM Usuarios;
SELECT * FROM polichinelo;

/* Apagar o banco antigo se tiver */
DROP DATABASE IF EXISTS agencia_carros;
CREATE DATABASE agencia_carros;

USE agencia_carros;

/* Tabela clientes */
CREATE TABLE clientes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    endereco VARCHAR(100)
);

/* Tabela veiculos */
CREATE TABLE veiculos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano INT,
    preco DECIMAL(10,2),
    cor VARCHAR(20)
);

/* Tabela vendas */
CREATE TABLE vendas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    veiculo_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
);

/* Inserindo clientes */
INSERT INTO clientes (nome, email, telefone, endereco) VALUES
('Osmar Zafalon', 'osmar.zafalon@gmail.com', '(11)998345774', 'Padre Donizetti, 28'),
('Silvana da Silva', 'silvana@gmail.com', '(11)995345879', 'C. Costa, 55');

/* Inserindo veículos */
INSERT INTO veiculos (marca, modelo, ano, preco, cor) VALUES
('Volkswagen', 'Gol', 2019, 42000.00, 'Prata'),
('Chevrolet', 'Onix', 2020, 55000.00, 'Branco'),
('Fiat', 'Argo', 2021, 58000.00, 'Vermelho'),
('Ford', 'Ka', 2018, 39000.00, 'Preto'),
('Hyundai', 'HB20', 2022, 69000.00, 'Azul'),
('Toyota', 'Corolla', 2023, 135000.00, 'Prata'),
('Honda', 'Civic', 2021, 128000.00, 'Cinza'),
('Nissan', 'Kicks', 2020, 97000.00, 'Branco'),
('Jeep', 'Renegade', 2019, 105000.00, 'Verde'),
('Renault', 'Sandero', 2018, 37000.00, 'Preto'),
('Peugeot', '208', 2021, 63000.00, 'Azul'),
('Citroën', 'C3', 2020, 52000.00, 'Branco'),
('Fiat', 'Strada', 2022, 88000.00, 'Vermelho'),
('Chevrolet', 'Tracker', 2023, 125000.00, 'Cinza'),
('Volkswagen', 'T-Cross', 2022, 134000.00, 'Prata'),
('Hyundai', 'Creta', 2021, 118000.00, 'Branco'),
('Toyota', 'Hilux', 2023, 245000.00, 'Preto'),
('Honda', 'HR-V', 2022, 155000.00, 'Cinza'),
('Nissan', 'Versa', 2019, 62000.00, 'Vermelho'),
('Jeep', 'Compass', 2023, 198000.00, 'Branco');

/* Inserindo vendas (após os veículos já existirem) */
INSERT INTO vendas (cliente_id, veiculo_id, valor) VALUES
(1, 2, 90000.00);

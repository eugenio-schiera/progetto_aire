-- =========================================================
-- TABELLA STAZIONI
-- =========================================================
CREATE DATABASE IF NOT EXISTS aire_db;
USE aire_db;

CREATE TABLE stazione (
    id_amat INT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    id_arpa VARCHAR(20),
    inizio_operativita DATE NOT NULL,
    fine_operativita DATE,
    longitudine DOUBLE,
    latitudine DOUBLE
);

-- =========================================================
-- TABELLA INQUINANTI
-- =========================================================

CREATE TABLE inquinante (
    codice VARCHAR(20) PRIMARY KEY
);

-- =========================================================
-- RELAZIONE N:N STAZIONE <-> INQUINANTE
-- =========================================================

CREATE TABLE stazione_inquinante (
    stazione_id INT NOT NULL,
    inquinante_codice VARCHAR(20) NOT NULL,

    PRIMARY KEY (stazione_id, inquinante_codice),

    FOREIGN KEY (stazione_id)
        REFERENCES stazione(id_amat),

    FOREIGN KEY (inquinante_codice)
        REFERENCES inquinante(codice)
);

-- =========================================================
-- TABELLA MISURAZIONI
-- =========================================================

CREATE TABLE misurazione_giornaliera (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stazione_id INT NOT NULL,
    data DATE NOT NULL,
    inquinante_codice VARCHAR(20) NOT NULL,
    valore DECIMAL(10,2),

    FOREIGN KEY (stazione_id)
        REFERENCES stazione(id_amat),

    FOREIGN KEY (inquinante_codice)
        REFERENCES inquinante(codice),

    UNIQUE (stazione_id, data, inquinante_codice),

    FOREIGN KEY (stazione_id, inquinante_codice)
        REFERENCES stazione_inquinante(stazione_id, inquinante_codice)
);


-- =========================================================
-- INSERT STAZIONI
-- =========================================================

INSERT INTO stazione (
    id_amat,
    nome,
    id_arpa,
    inizio_operativita,
    fine_operativita,
    longitudine,
    latitudine
) VALUES
(1, 'p.le Abbiategrasso', '126', '1900-01-01', '2017-08-31', 9.18218994140625, 45.432300567627),
(2, 'via Pascal *', '100', '1900-01-01', '2099-12-31', 9.23478031158447, 45.4740982055664),
(3, 'viale Liguria', '107', '1900-01-01', '2099-12-31', 9.16944026947021, 45.4441986083984),
(4, 'viale Marche', '2', '1900-01-01', '2099-12-31', 9.19083976745605, 45.4962997436523),
(5, 'Parco Lambro', '124', '1900-01-01', '2017-08-31', 9.24730014801025, 45.4995994567871),
(6, 'via Senato *', '125', '1900-01-01', '2099-12-31', 9.19791984558105, 45.4705009460449),
(7, 'Verziere', '85', '1900-01-01', '2099-12-31', 9.19534015655518, 45.4635009765625),
(8, 'p.le Zavattari', '7', '1900-01-01', '2017-08-31', 9.141770362854, 45.4761009216309),
(9, 'via Juvara', '7', '1900-01-01', '2007-06-11', 9.22045040130615, 45.4734992980957);

-- =========================================================
-- INSERT INQUINANTI
-- =========================================================

INSERT INTO inquinante (codice) VALUES
('NO2'),
('SO2'),
('O3'),
('PM10'),
('PM25'),
('C6H6'),
('CO_8h');

-- =========================================================
-- RELAZIONI STAZIONE <-> INQUINANTE
-- =========================================================

INSERT INTO stazione_inquinante (
    stazione_id,
    inquinante_codice
) VALUES

-- stazione 1
(1, 'NO2'),

-- stazione 2
(2, 'SO2'),
(2, 'NO2'),
(2, 'O3'),
(2, 'PM10'),
(2, 'C6H6'),
(2, 'PM25'),

-- stazione 3
(3, 'CO_8h'),
(3, 'NO2'),

-- stazione 4
(4, 'CO_8h'),
(4, 'NO2'),
(4, 'PM10'),
(4, 'C6H6'),
(4, 'PM25'),

-- stazione 5
(5, 'NO2'),
(5, 'O3'),

-- stazione 6
(6, 'CO_8h'),
(6, 'NO2'),
(6, 'PM10'),
(6, 'C6H6'),
(6, 'PM25'),

-- stazione 7
(7, 'CO_8h'),
(7, 'NO2'),
(7, 'O3'),
(7, 'PM10'),

-- stazione 8
(8, 'CO_8h'),
(8, 'NO2'),
(8, 'C6H6'),

-- stazione 9
(9, 'SO2'),
(9, 'NO2'),
(9, 'O3'),
(9, 'PM10'),
(9, 'PM25');


LOAD DATA LOCAL INFILE 'C:\\progetto_aire\\data\\qaria_datoariagiornostazione_2026-05-19.csv'
INTO TABLE misurazione_giornaliera
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    stazione_id,
    data,
    inquinante_codice,
    @valore
)
SET valore = NULLIF(@valore, '');

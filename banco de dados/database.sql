CREATE TABLE categoria
(
 id_categoria int IDENTITY(1,1) PRIMARY KEY,
 nome_categoria varchar(30) NOT NULL ,
);

CREATE TABLE marca
(
 id_marca int IDENTITY(1,1) PRIMARY KEY,
 nome_marca varchar(50) NOT NULL ,
);

CREATE TABLE orgao
(
 id_orgao int IDENTITY(1,1) PRIMARY KEY,
 nome_orgao varchar(80) NOT NULL,
 uasg char(6) NOT NULL UNIQUE
);

CREATE TABLE fase_pregao
(
 id_fase int IDENTITY(1,1) PRIMARY KEY,
 nome_fase varchar(30) NOT NULL ,
);

CREATE TABLE pregao
(
 id_pregao int IDENTITY(1,1) PRIMARY KEY ,
 numero_pregao varchar(10) NOT NULL ,
 data_abertura datetime NOT NULL ,
 data_ata date,
 id_fase int NOT NULL ,
 id_orgao int NOT NULL,
 CONSTRAINT FK_orgao_pregao
	FOREIGN KEY (id_orgao)
	REFERENCES orgao (id_orgao)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
 CONSTRAINT FK_fase_pregao
	FOREIGN KEY (id_fase)
	REFERENCES fase_pregao (id_fase)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
);

CREATE TABLE item
(
 id_item int IDENTITY(1,1) PRIMARY KEY,
 item int NOT NULL,
 modelo varchar(45),
 quantidade	int,
 colocacao int,
 valor_ofertado decimal(11,2) NOT NULL,
 preco_custo decimal (11,2) NOT NULL,
 frete decimal (11,2) NOT NULL,
 fornecedor varchar(400),
 id_pregao int NOT NULL,
 id_marca int,
 id_categoria int,
 CONSTRAINT FK_marca_item
	FOREIGN KEY (id_marca)
	REFERENCES marca (id_marca)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
 CONSTRAINT FK_pregao_item
	FOREIGN KEY (id_pregao)
	REFERENCES pregao (id_pregao)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
 CONSTRAINT FK_categoria_item
	FOREIGN KEY (id_categoria)
	REFERENCES categoria (id_categoria)
	ON DELETE NO ACTION
	ON UPDATE CASCADE
);

CREATE TABLE fase_carona
(
 id_fase int IDENTITY(1,1) PRIMARY KEY,
 nome_fase varchar(30) NOT NULL ,
);

CREATE TABLE carona (
	id_carona int IDENTITY(1,1) PRIMARY KEY,
	data_carona date NOT NULL,
	id_pregao int NOT NULL,
	id_orgao int NOT NULL,
	id_fase int NOT NULL,
	CONSTRAINT FK_pregao_carona
		FOREIGN KEY (id_pregao)
		REFERENCES pregao (id_pregao)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	CONSTRAINT FK_orgao_carona
		FOREIGN KEY (id_orgao)
		REFERENCES orgao (id_orgao)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT FK_fase_carona
		FOREIGN KEY (id_fase)
		REFERENCES fase_carona (id_fase)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
);

CREATE TABLE item_carona
(
	id_item_carona int IDENTITY(1,1) PRIMARY KEY,
	quantidade int NOT NULL,
	valor_ofertado decimal(11,2) NOT NULL,
	id_carona int NOT NULL,
	id_item int NOT NULL,
	CONSTRAINT FK_item_item_carona
		FOREIGN KEY (id_item)
		REFERENCES item (id_item)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	CONSTRAINT FK_carona_item_carona
		FOREIGN KEY (id_carona)
		REFERENCES carona (id_carona)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
);

CREATE TABLE fase_empenho
(
 id_fase int IDENTITY(1,1) PRIMARY KEY,
 nome_fase varchar(30) NOT NULL ,
);

CREATE TABLE empenho
(
 id_empenho int IDENTITY(1,1) PRIMARY KEY,
 data_empenho date NOT NULL ,
 nota_empenho varchar(30) NULL,
 data_entrega date NULL,
 id_carona int NULL,
 id_pregao int NOT NULL,
 id_fase int NOT NULL,
 id_orgao int NULL,
CONSTRAINT FK_carona_empenho
	FOREIGN KEY (id_carona)
	REFERENCES carona (id_carona)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
CONSTRAINT FK_pregao_empenho
	FOREIGN KEY (id_pregao)
	REFERENCES pregao (id_pregao)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION,
CONSTRAINT FK_fase_empenho
	FOREIGN KEY (id_fase)
	REFERENCES fase_empenho (id_fase)
	ON DELETE NO ACTION
	ON UPDATE CASCADE,
CONSTRAINT FK_orgao_empenho
	FOREIGN KEY (id_orgao)
	REFERENCES orgao (id_orgao)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
);

CREATE TABLE item_empenho
(
 id_item_empenho int IDENTITY(1,1) PRIMARY KEY,
 quantidade int NOT NULL,
 modelo varchar(45) NULL,
 custo_unitario decimal(11,2),
 valor_ofertado decimal(11,2),
 id_marca int NULL,
 id_empenho int NOT NULL,
 id_item int NOT NULL,
CONSTRAINT FK_marca_item_empenho
	FOREIGN KEY (id_marca)
	REFERENCES marca (id_marca)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
CONSTRAINT FK_empenho_item_empenho
	FOREIGN KEY (id_empenho)
	REFERENCES empenho (id_empenho)
	ON DELETE CASCADE
	ON UPDATE CASCADE,
CONSTRAINT FK_item_item_empenho
	FOREIGN KEY (id_item)
	REFERENCES item (id_item)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION,
);

CREATE TABLE fase_reequilibrio
(
 id_fase int IDENTITY(1,1) PRIMARY KEY,
 nome_fase varchar(30) NOT NULL ,
);

CREATE TABLE reequilibrio 
(
	id_reequilibrio int IDENTITY(1,1) PRIMARY KEY,
	data_reequilibrio date NOT NULL,
	id_pregao int NOT NULL,
	id_orgao int NOT NULL,
	id_fase int NOT NULL,
	CONSTRAINT FK_pregao_reequilibrio
		FOREIGN KEY (id_pregao)
		REFERENCES pregao (id_pregao)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
	CONSTRAINT FK_orgao_reequilibrio
		FOREIGN KEY (id_orgao)
		REFERENCES orgao (id_orgao)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION,
	CONSTRAINT FK_fase_reequilibrio
		FOREIGN KEY (id_fase)
		REFERENCES fase_reequilibrio (id_fase)
		ON DELETE NO ACTION
		ON UPDATE CASCADE,
);

CREATE TABLE item_reequilibrio
(
	id_item_reequilibrio int IDENTITY(1,1) PRIMARY KEY,
	quantidade int NOT NULL,
	valor_novo decimal(11,2) NOT NULL,
	valor_ofertado decimal(11,2) NOT NULL,
	id_reequilibrio int NOT NULL,
	CONSTRAINT FK_reequilibrio_item_reequilibrio
		FOREIGN KEY (id_reequilibrio)
		REFERENCES reequilibrio (id_reequilibrio)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
);
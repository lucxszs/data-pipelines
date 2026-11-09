-- Fictitious bronze rows, so `dbt build` runs in CI without Airflow or the real sources.
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE bronze.bacen_ptax (data_hora_cotacao TEXT PRIMARY KEY, payload JSONB NOT NULL, loaded_at TIMESTAMPTZ NOT NULL DEFAULT now());
INSERT INTO bronze.bacen_ptax VALUES
    ('2026-10-01 13:06:00.000', '{"cotacaoCompra": 5.4012, "cotacaoVenda": 5.4018, "dataHoraCotacao": "2026-10-01 13:06:00.000"}'),
    ('2026-10-02 13:06:00.000', '{"cotacaoCompra": 5.4210, "cotacaoVenda": 5.4216, "dataHoraCotacao": "2026-10-02 13:06:00.000"}');

CREATE TABLE bronze.cnpjpw_empresas (cnpj TEXT PRIMARY KEY, payload JSONB NOT NULL, loaded_at TIMESTAMPTZ NOT NULL DEFAULT now());
INSERT INTO bronze.cnpjpw_empresas VALUES
    ('11111111000191', '{"cnpj_base": "11111111", "nome_empresarial": "EMPRESA EXEMPLO A", "nome_fantasia": "", "data_inicio_atividade": "2026-10-01", "identificador_descricao": "Matriz", "cnae_fiscal_principal": 6201501, "cnae_fiscal_principal_descricao": "Desenvolvimento de programas", "natureza_juridica_desc": "Empresário (Individual)", "porte_empresa_descricao": "Micro Empresa", "capital_social": 5000.0, "situacao_cadastral_descricao": "Ativa", "uf": "SP", "municipio": 7107, "municipio_desc": "SAO PAULO", "opcao_simples": true, "opcao_mei": true, "ddd1": "11", "telefone_1": "30000000", "correio_eletronico": "A@EXEMPLO.COM", "socios": null}'),
    ('22222222000180', '{"cnpj_base": "22222222", "nome_empresarial": "EMPRESA EXEMPLO B LTDA", "nome_fantasia": "EXEMPLO B", "data_inicio_atividade": "2026-10-01", "identificador_descricao": "Matriz", "cnae_fiscal_principal": 6201501, "cnae_fiscal_principal_descricao": "Desenvolvimento de programas", "natureza_juridica_desc": "Sociedade Empresária Limitada", "porte_empresa_descricao": "Demais", "capital_social": 50000.0, "situacao_cadastral_descricao": "Ativa", "uf": "SP", "municipio": 7107, "municipio_desc": "SAO PAULO", "opcao_simples": null, "opcao_mei": null, "ddd1": null, "telefone_1": null, "correio_eletronico": null, "socios": [{"nome": "FULANO DE TAL", "cnpj_cpf": "***000000**", "data_entrada_sociedade": "2026-10-01"}, {"nome": "BELTRANO SILVA", "cnpj_cpf": "***111111**", "data_entrada_sociedade": "2026-10-01"}]}'),
    ('33333333000172', '{"cnpj_base": "33333333", "nome_empresarial": "EMPRESA EXEMPLO C LTDA", "nome_fantasia": null, "data_inicio_atividade": "2026-10-02", "identificador_descricao": "Filial", "cnae_fiscal_principal": 4781400, "cnae_fiscal_principal_descricao": "Comércio de vestuário", "natureza_juridica_desc": "Sociedade Empresária Limitada", "porte_empresa_descricao": "Micro Empresa", "capital_social": 1000.0, "situacao_cadastral_descricao": "Ativa", "uf": "MG", "municipio": 4123, "municipio_desc": "BELO HORIZONTE", "opcao_simples": false, "opcao_mei": false, "ddd1": null, "telefone_1": null, "correio_eletronico": null, "socios": [{"nome": "CICLANA SOUZA", "cnpj_cpf": "***222222**", "data_entrada_sociedade": "2026-10-02"}]}');

CREATE TABLE bronze.gov_pep (
    cpf TEXT, nome_pep TEXT, sigla_funcao TEXT, descricao_funcao TEXT, nivel_funcao TEXT,
    nome_orgao TEXT, data_inicio_exercicio TEXT, data_fim_exercicio TEXT, data_fim_carencia TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
INSERT INTO bronze.gov_pep VALUES
    ('***.111.111-**', 'FULANO DE TAL', 'DAS', 'DIRETOR', '101.5', 'MINISTERIO A', '01/02/2023', 'Não informada', 'Não informada'),
    ('***.222.222-**', 'BELTRANO SILVA', 'CNE', 'ASSESSOR', '102.3', 'MINISTERIO A', '15/03/2022', '10/01/2024', '10/07/2024'),
    ('***.333.333-**', 'CICLANA SOUZA', 'DAS', 'COORDENADORA', '101.4', 'AGENCIA B', '05/05/2021', 'Não informada', 'Não informada');

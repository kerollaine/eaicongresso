CREATE OR REPLACE FUNCTION importar_tramitacao(id_proposicao integer, data date) RETURNS void AS $$

BEGIN
	INSERT INTO tramitacao(
            id_proposicao, data)
    VALUES (id_proposicao, data);
    
    PERFORM atualiza_status_proposicao(id_proposicao);

END;

$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION atualiza_status_proposicao(id integer) RETURNS void AS $$

BEGIN
	IF EXISTS (SELECT * FROM importacao_proposicao where id_proposicao = id) THEN
		UPDATE importacao_proposicao
   			SET desatualizada=true
 			WHERE id_proposicao = id;
 	ELSE
 		INSERT INTO importacao_proposicao(
 			id_proposicao, desatualizada)
 		VALUES (id, true);
	END IF;
END;

$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION obter_proposicao(p_id integer, p_nome varchar, p_numero integer, p_ano integer, 
											p_data_ap date, p_data_despacho date, p_ementa text, p_explicacao_ementa text,
											p_indexacao text, p_link varchar, p_autor varchar, p_autoruf varchar, p_autorpartido varchar, 
											p_tipo varchar, p_tiposigla varchar, p_situacao varchar, p_tema text)
	RETURNS void AS $$

	DECLARE
		id_autor integer;
		id_tipo integer;
		id_status integer;
		i text;
		id_temas integer[];
		id_tema_inserido integer;
		contador integer;
		desc_tema varchar;

	BEGIN
		/*
		Bloco que verifica se o autor já existe ou insere um novo, e retorna o id.
		*/
		SELECT id INTO id_autor FROM autor WHERE nome = p_autor;
		IF id_autor IS NULL THEN
			INSERT INTO autor(nome, partido, uf) 
			VALUES (p_autor, p_autorpartido, p_autoruf) RETURNING id INTO id_autor;
		END IF;

		/*
		Bloco que verifica se o tipo de proposição já existe ou insere um novo, e retorna o id.
		*/
		SELECT id INTO id_tipo FROM tipo_proposicao WHERE sigla = p_tiposigla;
		IF id_tipo IS NULL THEN
			INSERT INTO tipo_proposicao(sigla, descricao) 
			VALUES (p_tiposigla, p_tipo) RETURNING id INTO id_tipo;
		END IF;

		/*
		Bloco que verifica se a situação já existe ou insere uma nova, e retorna o id.
		*/
		SELECT id INTO id_status FROM situacao WHERE descricao = p_situacao;
		IF id_status IS NULL THEN
			INSERT INTO situacao(descricao) 
			VALUES (p_situacao) RETURNING id INTO id_status;
		END IF;

		/* Bloco que separa o tema, verifica se já está cadastrado e caso negativo, o cadastra */
		contador := -1;
		FOR i IN
   				SELECT regexp_split_to_table(p_tema, '[,;]')
		LOOP

			contador := contador + 1;
			
			SELECT TRIM(i) INTO desc_tema;
			id_temas[contador] := (SELECT id FROM tema WHERE descricao = desc_tema);
  			IF id_temas[contador] IS NULL THEN
				INSERT INTO tema(descricao) 
					VALUES (desc_tema) RETURNING id INTO id_tema_inserido;
				id_temas[contador] := id_tema_inserido;
			END IF;
		
		END LOOP;


		IF EXISTS (SELECT id FROM proposicao where id = p_id) THEN
			UPDATE proposicao
   				SET nome=p_nome, numero=p_numero, ano=p_ano, data_apresentacao=p_data_ap, data_ultimo_despacho=p_data_despacho, 
		       ementa=p_ementa, explicacao_ementa=p_explicacao_ementa, indexacao=p_indexacao, link_teor=p_link, id_autor_principal=id_autor, 
		       id_tipo_proposicao=id_tipo, id_situacao=id_status
 			WHERE id = p_id;

 		ELSE 

			INSERT INTO proposicao(
	            id, nome, numero, ano, data_apresentacao, data_ultimo_despacho, 
	            ementa, explicacao_ementa, indexacao, link_teor, id_autor_principal, 
	            id_tipo_proposicao, id_situacao)
	    		
			VALUES (p_id, p_nome, p_numero, p_ano, p_data_ap, p_data_despacho, 
	            p_ementa, p_explicacao_ementa, p_indexacao, p_link, id_autor, 
	            id_tipo, id_status);

		END IF;

		DELETE FROM tema_proposicao WHERE id_proposicao = p_id;
		WHILE contador >= 0 LOOP
			INSERT INTO tema_proposicao(id_tema, id_proposicao)
			VALUES (id_temas[contador], p_id);
						
			contador := contador - 1;
		END LOOP;
		
		UPDATE importacao_proposicao SET desatualizada=false
 			WHERE id_proposicao=p_id;

	END;

$$ LANGUAGE plpgsql;
from pandas import DataFrame,to_datetime
from mssql.singleton import Singleton

class DatabaseFacade:
    """
        Fachada de base de datos, crea conexion con un singleton a mssql, y define las operaciones dentro de esta como funciones independientes
    """
    def __init__(self, connection_string: str):
        self.db = Singleton(connection_string)

    def fetch_periodo_facturacion(self) -> DataFrame:
        """
            Obtiene las plantas disponibles en base de datos
        """
        query = """
            SELECT 
                fecha_inicio, fecha_fin
            FROM 
                cat_periodo_facturacion_consumo
            WHERE
                CONVERT(DATE, GETDATE() at time zone 'UTC' at time zone 'Central Standard Time (Mexico)') BETWEEN fecha_inicio AND fecha_fin
        """
        return self.db.executable_query(query)

    def fetch_clave_carga(self) -> DataFrame:
        """
            Obtiene las plantas disponibles en base de datos
        """
        query = """
            SELECT
                cc.clave clave_carga
            FROM
                tbl_clave_carga cc
            ORDER BY
                clave_carga
        """
        return self.db.executable_query(query)
        
    def fetch_rpus(self) -> DataFrame:
        """
            Obtiene las plantas disponibles en base de datos
        """
        query = """
            /*SELECT
                crs.alux_customuser alux_customuser, 
                ucm.id AS unidad_consumo_id,
                ucm.identificador AS Equipo,
                c.nombre AS cliente,
                -- cc.clave AS clave_de_carga,
                z.nombre zona_de_carga,
                cc.id tbl_clave_carga_id,
                cc.clave AS clave_de_carga,
                -- CAST(ucm.rpu AS FLOAT) AS rpu,
                ucm.rpu,
                ca.perdidas,
                ca.
                fp.perdida_tecnica_estimada,
                fp.perdida_estimada_total
            FROM 
                tbl_unidad_consumo ucm
            INNER JOIN
                tbl_cliente_razon_social crs 
                ON ucm.tbl_cliente_razon_social_id = crs.id
            INNER JOIN
                tbl_cliente c 
                ON crs.tbl_cliente_id = c.id
            LEFT JOIN
                tbl_zona z 
                ON z.id = ucm.tbl_zona_id
            LEFT JOIN
                tbl_clave_carga cc ON cc.id = ucm.tbl_clave_carga_id
            LEFT JOIN
                tbl_division d 
                ON d.id = z.tbl_division_id
            LEFT JOIN
                tbl_factor_perdida fp 
                ON d.id = fp.tbl_division_id
            LEFT JOIN
                tbl_detalle_costo_anual ca 
                ON ca.tbl_unidad_consumo_id = ucm.id
            WHERE 
                ucm.activo = 1;*/
        SELECT
            info.rpu rpu, 
            info.fee, 
            info.precio_cels costo_cels, 
            info.zona_de_carga zona, 
            info.rap, 
            info.precio_potencia, 
            info.costo_cobertura, 
            info.volumen_cobertura,
            UPPER(Nodo_cobertura_solar) Nodo_cobertura_solar, 
            Mercado_Solar,
            UPPER(Nodo_cobertura_eolica) Nodo_cobertura_eolica, 
            Mercado_eolico,
            UPPER(Nodo_cobertura_24hrs) Nodo_cobertura_24hrs, 
            Mercado_24hrs,
            z.Region,
            info.demanda_contratada_mw demanda_mw,
            d.id region_id,
            ucm.id tbl_unidad_consumo_id,
            info.clave_de_carga,
            cc.id tbl_clave_carga_id
        FROM (	
            SELECT
                DISTINCT 
                icc.rpu rpu, 
                icc.fee, 
                icc.precio_cels, 
                zona_de_carga, 
                icc.rap, 
                icc.precio_potencia, 
                icc.costo_cobertura, 
                icc.volumen_cobertura,
                ieo.demanda_contratada_mw,
                ieo.clave_de_carga,
                Nodo_cobertura_solar, 
                Mercado_Solar,
        	    Nodo_cobertura_eolica, 
                Mercado_eolico,
        	    Nodo_cobertura_24hrs, 
                Mercado_24hrs
            FROM
        		informacion_contratos_clientes icc
        	INNER JOIN
        	    informacion_entrada_operacion ieo ON ieo.rpu = icc.rpu
            WHERE
        	activo = 1
        ) info
        LEFT JOIN
            Zonas_Regiones z ON REPLACE(UPPER(z.[Zona De Carga]),' ','') = REPLACE(UPPER(info.zona_de_carga),' ','') COLLATE Latin1_General_CI_AI 
        LEFT JOIN
            tbl_division d ON REPLACE(UPPER(d.nombre),' ','') = REPLACE(UPPER(z.Region),' ','') COLLATE Latin1_General_CI_AI 
        LEFT JOIN
            tbl_unidad_consumo ucm ON info.rpu = CAST(ucm.rpu AS FLOAT)
        LEFT JOIN
            tbl_clave_carga cc ON cc.clave = info.clave_de_carga
        """
        return self.db.executable_query(query)

    def fetch_cobros_estado_cuenta(self, fecha_inicio: str, fecha_fin: str) -> DataFrame:
        """
            Obtiene la generacion de cada planta del ultimo mes, ajustando con su intervalo, ya sea 5minutal o 15minutal
        """
        query = f"""
            SELECT 
                fecha,
                hora,
                clave,
                tbl_clave_carga_id,
                COALESCE([Servicios Conexos], 0) [Servicios Conexos],
                COALESCE([Transmision], 0) [Transmision],
                COALESCE([Distribucion], 0) [Distribucion],
                COALESCE([Operacion Cenace], 0) [Operacion Cenace],
                COALESCE([GSI], 0) [GSI],
                COALESCE([Otros Conceptos], 0) [Otros Conceptos]
            FROM 
            (
                SELECT
                    CONVERT(DATE, Fecha_Operacion) AS fecha,
                    edc.cliente AS clave,
                    cc.id tbl_clave_carga_id,
                    CASE 
                                WHEN folios.Concepto IN ('Cargos de Garantía de Suficiencia de Ingresos MDA', 'Cargos de Garantía de Suficiencia de Ingresos MTR') THEN 'GSI'
                                WHEN folios.Concepto IN ('Contribuciones de Servicios de Reserva  MDA', 'Contribuciones de Servicios de Reserva MTR','Servicios Conexos no Incluidos en el Mercado Eléctrico Mayorista') THEN 'Servicios Conexos'
                            WHEN folios.Concepto IN ('Operación del Mercado y Servicio de Control del Sistema') THEN 'Operacion Cenace'
                            WHEN folios.Concepto IN ('Servicios de Distribución') THEN 'Distribucion'
                            WHEN folios.Concepto IN ('Servicios de Transmisión') THEN 'Transmision'
                            WHEN folios.Concepto IN ('Cargos de Energía MDA', 'Cargos de Energía MTR') THEN 'Energia'
                        ELSE 
                                'Otros conceptos' 
                    END AS concepto,
                    COALESCE(SUM([Monto]), 0) AS monto
                FROM 
                    [dbo].[Historico_EDC_Clientes_XML] AS edc
                INNER JOIN 
                    Folios_EDC AS folios ON folios.Folio = edc.Folio AND folios.[Terminacion] = edc.cuenta
                LEFT JOIN
                    tbl_clave_carga cc ON cc.clave = edc.cliente
                WHERE	
                    Cuenta = 'C00'
                AND 
                    CONVERT(DATE, Fecha_Operacion) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                GROUP BY
                    CONVERT(DATE, Fecha_Operacion),
                    cc.id,
                    edc.cliente,
                    CASE 
                                WHEN folios.Concepto IN ('Cargos de Garantía de Suficiencia de Ingresos MDA', 'Cargos de Garantía de Suficiencia de Ingresos MTR') THEN 'GSI'
                                WHEN folios.Concepto IN ('Contribuciones de Servicios de Reserva  MDA', 'Contribuciones de Servicios de Reserva MTR','Servicios Conexos no Incluidos en el Mercado Eléctrico Mayorista') THEN 'Servicios Conexos'
                            WHEN folios.Concepto IN ('Operación del Mercado y Servicio de Control del Sistema') THEN 'Operacion Cenace'
                            WHEN folios.Concepto IN ('Servicios de Distribución') THEN 'Distribucion'
                            WHEN folios.Concepto IN ('Servicios de Transmisión') THEN 'Transmision'
                            WHEN folios.Concepto IN ('Cargos de Energía MDA', 'Cargos de Energía MTR') THEN 'Energia'
                        ELSE 
                                'Otros conceptos' 
                    END
            ) AS sourceTable
            PIVOT
            (
            SUM(monto)
            FOR concepto IN ([GSI], [Servicios Conexos], [Otros Conceptos], [Operacion Cenace], [Distribucion], [Transmision])
            ) AS pivotTable
            CROSS JOIN
                cat_hora h
            ORDER BY
                fecha, clave, hora
        """
        
        edc: DataFrame = self.db.executable_query(query)
        
        edc['fecha'] = to_datetime(edc['fecha'])
        
        return edc

    def fetch_lecturas_periodo_facturacion(self, fecha_inicio: str, fecha_fin: str) -> DataFrame:
        """
            Obtiene la generacion de cada planta del ultimo mes, ajustando con su intervalo, ya sea 5minutal o 15minutal
        """
        query = f"""
            SELECT
                tbl_clave_carga_id,
                tbl_unidad_consumo_id,
                fecha_2 AS fecha,
                hora AS hora,
                SUM(com.Kwhe) / 1000 AS Mwhe,
                SUM(com.Kvarh) / 1000 AS Mvarh
            FROM 
                his_lectura_consumo com
            INNER JOIN
                tbl_unidad_consumo ucm ON ucm.id = tbl_unidad_consumo_id
            WHERE
                com.fecha_2 BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            GROUP BY 
                tbl_clave_carga_id,
                tbl_unidad_consumo_id,
                fecha_2,
                hora
            ORDER BY
                tbl_unidad_consumo_id,
                fecha,
                hora;
        """
        
        
        lect: DataFrame = self.db.executable_query(query)
        
        lect['fecha'] = to_datetime(lect['fecha'])
        
        return lect
      
    def fetch_ccve(self, fecha_inicio: str, fecha_fin: str) -> DataFrame:
        """
            Obtiene las plantas disponibles en base de datos
        """
        query = f"""
                SELECT 
                    CONVERT(DATE, Fecha) fecha,
                    Hora hora,
                    Clave_de_carga Clave_de_carga,
	                cc.id tbl_clave_carga_id,
                    Compra_MDA,
                    [Compra/Venta_MTR] Compra_Venta_MTR,
                    Precio_MTR,
                    Monto AS Monto_MTR,
                    Precio_MDA,
                    Monto_MDA
                FROM 
                    [dbo].Clientes_compra_venta_energia_XML ccve
	            LEFT JOIN
		            tbl_clave_carga cc ON cc.clave = ccve.Clave_de_carga
                WHERE
                    fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}';
        """
        
        ccve: DataFrame = self.db.executable_query(query)
        
        ccve['fecha'] = to_datetime(ccve['fecha'])
        
        return ccve
    
    def fetch_tipo_cambio(self, fecha_inicio: str, fecha_fin: str) -> DataFrame:
        """
            Obtiene la generacion de cada planta del ultimo mes, ajustando con su intervalo, ya sea 5minutal o 15minutal
        """
        
        query = f"""
                SELECT
                    f.fecha, h.hora,
                    COALESCE(tp.precio, (SELECT AVG(precio) precio FROM tbl_tipo_cambio WHERE cat_tipo_cambio_id = 101 AND DATEPART(M, fecha) = DATEPART(M, f.fecha))) precio
                FROM
                    cat_fecha f
                CROSS JOIN
                    cat_hora h
                LEFT JOIN
                    tbl_tipo_cambio tp ON tp.fecha = f.fecha AND tp.hora = h.hora AND tp.cat_tipo_cambio_base_id = 101
                WHERE	
                    f.fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}';
        """
            
            
        tipo_cambio: DataFrame = self.db.executable_query(query)
        
        tipo_cambio['fecha'] = to_datetime(tipo_cambio['fecha'])
        
        return tipo_cambio
    
    
    def fetch_coberturas(self) -> DataFrame:
        """
            Obtiene la generacion de cada planta del ultimo mes, ajustando con su intervalo, ya sea 5minutal o 15minutal
        """
        
        query = f"""
            SELECT
                ucm.id tbl_unidad_consumo_id,
                pt.Mes,
                DATEPART(DAY, d.Fecha) Dia,
                d.Hora,
                COALESCE(pt.[solar], 0) * COALESCE(d.Cobertura_Solar_MWh, 0) Cobertura_Solar_MWh,
                COALESCE(pt.[eolico], 0) * COALESCE(d.Cobertura_Eolica_MWh, 0) Cobertura_Eolica_MWh,
                COALESCE(pt.[24hrs], 0) * COALESCE(d.Cobertura_24h_MWh, 0) Cobertura_24h_MWh
            FROM
                view_porcentaje_cobertura_por_tecnologia pct 
                PIVOT 
                    (
                        SUM(total)
                        FOR tecnologia IN ([solar], [eolico], [24hrs])
                    ) AS pt	
            LEFT JOIN
                diponibilidad_horaria_cobertura_xml d ON d.Mes = pt.mes
            LEFT JOIN
	            tbl_unidad_consumo ucm ON CAST(ucm.rpu AS bigint) = CAST(pt.rpu AS bigint)
        """

        return self.db.executable_query(query)
    	
    

    def merge_data(self, planta_id, data_imputada: DataFrame) -> None:
        """
            Trabaja un Merge con la información corregida y la original
        """
        self.db.procedure(f"""
            EXEC update_generacion_planta {planta_id}, '{data_imputada.to_json(orient="records")}'          
        """)

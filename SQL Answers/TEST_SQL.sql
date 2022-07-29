--¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año?
SELECT aeropuertos.nombre_aerolinea, COUNT(viajes_info.id_aeropuerto) NUM_MOVIMIENTOS
  FROM viajes_info
  JOIN aeropuertos
  ON viajes_info.id_aeropuerto = aeropuertos.id_aeropuerto
GROUP BY aeropuertos.nombre_aerolinea
HAVING COUNT(viajes_info.id_aeropuerto)  = (SELECT MAX(COUNT(id_aeropuerto))
                                    FROM viajes_info
                                   GROUP BY id_aeropuerto);
                                   


--  ¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año?
SELECT aerolinea.nombre_aerolinea, COUNT(viajes_info.id_aerolinea) NUM_MOVIMIENTOS
  FROM viajes_info
  JOIN aerolinea
  ON viajes_info.id_aerolinea = aerolinea.id_aerolinea
GROUP BY aerolinea.nombre_aerolinea
HAVING COUNT(viajes_info.id_aerolinea)  = (SELECT MAX(COUNT(id_aerolinea))
                                    FROM viajes_info
                                   GROUP BY id_aerolinea);
                                   
                                   
--  ¿En qué día se han tenido mayor número de vuelos?

SELECT dia, COUNT(dia) NUM_VUELOS
  FROM viajes_info
 GROUP BY dia
HAVING COUNT(dia) = (SELECT MAX(COUNT(dia))
                       FROM viajes_info
                       GROUP BY dia);
                       
                       
--  ¿Cuáles son las aerolíneas que tienen mas de 2 vuelos por día?
/*
Esta query está compleja porque la subquery toma en cuenta que si una aerolinea tiene algún día donde tuve 2 o menos vuelos no cuenta
Porque la sig  query si hay algunas que fallaron en algín día y en uno tuvieron más de 2 vuelos igual los cuenta

SELECT aerolinea.nombre_aerolinea, viajes_info.dia, COUNT(viajes_info.id_aerolinea) NUM_MOVIMIENTOS
  FROM viajes_info
  JOIN aerolinea
  ON viajes_info.id_aerolinea = aerolinea.id_aerolinea
GROUP BY aerolinea.nombre_aerolinea, viajes_info.dia
HAVING COUNT(viajes_info.id_aerolinea) > 2;
*/
SELECT aerolinea.nombre_aerolinea, viajes_info.dia, COUNT(viajes_info.id_aerolinea) NUM_MOVIMIENTOS
  FROM viajes_info
  JOIN aerolinea
  ON viajes_info.id_aerolinea = aerolinea.id_aerolinea
GROUP BY aerolinea.nombre_aerolinea, viajes_info.dia
HAVING aerolinea.nombre_aerolinea NOT IN (SELECT aerolinea.nombre_aerolinea
                                            FROM viajes_info
                                            JOIN aerolinea
                                              ON viajes_info.id_aerolinea = aerolinea.id_aerolinea
                                            GROUP BY aerolinea.nombre_aerolinea, viajes_info.dia
                                            HAVING COUNT(viajes_info.id_aerolinea) <= 2)

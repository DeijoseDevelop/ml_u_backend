package db

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/Juan-Barraza/apiGoMl/config"
	_ "github.com/lib/pq"
)

func Connect() *sql.DB {
	log.Println("Conectando con la base de datos usando los siguientes parámetros:")
	log.Printf("Usuario: %s, Host: %s, Puerto: %s, Base de datos: %s",
		config.POSTGRES_USER, config.DB_HOST, config.DB_PORT, config.POSTGRES_DB)

	connStr := fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		config.POSTGRES_USER, config.POSTGRES_PASSWORD, config.DB_HOST, config.DB_PORT, config.POSTGRES_DB)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Error conectando la base de datos")
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Error al hacer ping a la base de datos:", err)
	}
	log.Println("Conexion Exitosa")

	return db
}

func CheckTables() {
	database := Connect()
	if database == nil {
		log.Fatal("Error: No se pudo conectar a la base de datos")
	}
	defer database.Close()

	rows, err := database.Query("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
	if err != nil {
		log.Println("Error verificando tablas:", err)
		return
	}
	defer rows.Close()

	log.Println("Tablas existentes:")
	foundTables := false
	for rows.Next() {
		var tableName string
		err := rows.Scan(&tableName)
		if err != nil {
			log.Println("Error escaneando fila:", err)
			return
		}
		foundTables = true
		log.Println("Tabla:", tableName)
	}

	if !foundTables {
		log.Println("No se encontraron tablas en la base de datos")
	}

	if err := rows.Err(); err != nil {
		log.Println("Error iterando las filas:", err)
	}
}

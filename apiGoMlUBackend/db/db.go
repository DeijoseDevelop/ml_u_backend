package db

import (
	"database/sql"

	"log"

	"github.com/Juan-Barraza/apiGoMl/config"
	_ "github.com/mattn/go-sqlite3"
)

func Connect() *sql.DB {
	db, err := sql.Open("sqlite3", config.DB_PATH)
	if err != nil {
		log.Fatal("Error conectando a la base de datos:", err)
	}

	return db
}

func CheckTables() {
	database := Connect()
	defer database.Close()

	rows, err := database.Query("SELECT name FROM sqlite_master WHERE type='table'")
	if err != nil {
		log.Fatal("Error verificando tablas:", err)
	}
	defer rows.Close()

	log.Println("Tablas existentes:")
	for rows.Next() {
		var tableName string
		rows.Scan(&tableName)
		log.Println("Tabla:", tableName)
	}
}
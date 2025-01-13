package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

var (
	SECRET_KEY        string
	POSTGRES_USER     string
	POSTGRES_PASSWORD string
	POSTGRES_DB       string
	DB_HOST           string
	DB_PORT           string
	// DB_PATH string
)

func LoadEnv() {
	err := godotenv.Load("./.env")
	if err != nil {
		log.Fatal("Error cargando el archivo .env")
	}
	log.Println(".env cargado correctamente")

	// Asignar variables de entorno
	SECRET_KEY = os.Getenv("JWT_SECRET_KEY")
	POSTGRES_USER = os.Getenv("POSTGRES_USER")
	POSTGRES_PASSWORD = os.Getenv("POSTGRES_PASSWORD")
	POSTGRES_DB = os.Getenv("POSTGRES_DB")
	DB_HOST = os.Getenv("DB_HOST")
	DB_PORT = os.Getenv("DB_PORT")
	// DB_PATH = os.Getenv("DB_PATH")
}

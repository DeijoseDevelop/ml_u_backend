package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

var (
	SECRET_KEY string
	DB_PATH    string
)

func LoadEnv() {
	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatal("Error cargando el archivo .env")
	}

	// Asignar variables de entorno
	SECRET_KEY = os.Getenv("JWT_SECRET_KEY")
	DB_PATH = os.Getenv("DB_PATH")
}

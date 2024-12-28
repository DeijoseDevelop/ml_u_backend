package main

import (
	"encoding/json"
	"log"
	"time"

	"github.com/Juan-Barraza/apiGoMl/config"
	"github.com/Juan-Barraza/apiGoMl/db"
	"github.com/Juan-Barraza/apiGoMl/routes"
	"github.com/gofiber/fiber/v3"
)

func main() {
	time.Sleep(5 * time.Second)

	config.LoadEnv()

	// conectar a la BD
	dbConn := db.Connect()
	db.CheckTables()

	app := fiber.New(fiber.Config{
		JSONEncoder:   json.Marshal,
		JSONDecoder:   json.Unmarshal,
		CaseSensitive: true,
		ServerHeader:  "MyFiberApp",
	})

	routes.SetUpRoutes(app, dbConn)

	// Iniciar el servidor en un goroutine
	if err := app.Listen(":8000"); err != nil {
		log.Fatalf("no se pudo iniciar el servidor: %v", err)
	}

	dbConn.Close()
}

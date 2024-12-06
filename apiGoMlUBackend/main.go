package main

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/Juan-Barraza/apiGoMl/config"
	"github.com/Juan-Barraza/apiGoMl/db"
	"github.com/Juan-Barraza/apiGoMl/routes"
	"github.com/gofiber/fiber/v3"
)

func main() {

	config.LoadEnv()

	// conectar a la BD
	dbConn := db.Connect()
	defer dbConn.Close()
	db.CheckTables()

	app := fiber.New(fiber.Config{
		JSONEncoder:   json.Marshal,
		JSONDecoder:   json.Unmarshal,
		CaseSensitive: true,
		ServerHeader:  "MyFiberApp",
	})

	routes.SetUpRoutes(app, dbConn)

	// Manejo de señales de interrupción (Ctrl+C)
	contx, sleep := signal.NotifyContext(context.Background(), os.Interrupt)
	defer sleep()

	// Iniciar el servidor en un goroutine
	go func() {
		if err := app.Listen(":8000"); err != nil {
			log.Fatalf("no se pudo iniciar el servidor: %v", err)
		}
	}()

	<-contx.Done()
	log.Println("interruption signal")

	time.Sleep(3 * time.Second)
	log.Println("El servidor se detuvo correctamente.")

}

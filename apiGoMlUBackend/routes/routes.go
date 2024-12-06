package routes

import (
	"database/sql"

	"github.com/Juan-Barraza/apiGoMl/controllers"
	"github.com/Juan-Barraza/apiGoMl/middleware"
	"github.com/Juan-Barraza/apiGoMl/repositories"
	"github.com/Juan-Barraza/apiGoMl/services"
	"github.com/gofiber/fiber/v3"
)

func SetUpRoutes(app *fiber.App, db *sql.DB) {
	dataRepo := repositories.NewDataRepository(db)
	dataService := services.NewDataService(dataRepo)
	dataController := controllers.NewDataController(dataService)
	app.Use(middleware.JWTMiddleware())

	app.Get("/api/v1/data", dataController.GetUsers)
}

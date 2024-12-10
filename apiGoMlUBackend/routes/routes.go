package routes

import (
	"database/sql"

	"github.com/Juan-Barraza/apiGoMl/controllers"
	"github.com/Juan-Barraza/apiGoMl/middleware"
	"github.com/Juan-Barraza/apiGoMl/repositories"
	"github.com/Juan-Barraza/apiGoMl/services"
	"github.com/gofiber/fiber/v3"
	"github.com/gofiber/fiber/v3/middleware/cors"
)

func SetUpRoutes(app *fiber.App, db *sql.DB) {
	app.Use(cors.New(cors.Config{
		AllowOrigins: []string{"*"},
		AllowHeaders: []string{"Origin, Content-Type, Accept, Authorization"},
		AllowMethods: []string{
			fiber.MethodGet,
			fiber.MethodPost,
			fiber.MethodHead,
			fiber.MethodPut,
			fiber.MethodDelete,
			fiber.MethodPatch,
			fiber.MethodOptions,
		},
	}))
	app.Use(middleware.JWTMiddleware())
	app.Use(func(c fiber.Ctx) error {
		err := c.Next()
		if err != nil {
			code := fiber.StatusInternalServerError
			if e, ok := err.(*fiber.Error); ok {
				code = e.Code
			}
			return c.Status(code).JSON(fiber.Map{
				"error": err.Error(),
			})
		}
		return nil
	})

	dataRepo := repositories.NewDataRepository(db)
	dataService := services.NewDataService(dataRepo)
	dataController := controllers.NewDataController(dataService)

	app.Get("/api/v1/ingress_records", dataController.GetCombinedInformation)
	app.Get("/api/v1/export_xlsx", dataController.ExportXslx)
}

package controllers

import (
	"github.com/Juan-Barraza/apiGoMl/services"
	"github.com/gofiber/fiber/v3"
)

type DataController struct {
	Service *services.DataService
}

func NewDataController(service *services.DataService) *DataController {
	return &DataController{Service: service}
}

func (uc *DataController) GetUsers(c fiber.Ctx) error {
	users, err := uc.Service.GetUsers()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to fetch users"})
	}
	return c.Status(fiber.StatusOK).JSON(users)
}

package controllers

import (
	"bytes"
	"log"
	"time"

	"github.com/Juan-Barraza/apiGoMl/services"
	"github.com/Juan-Barraza/apiGoMl/utils"
	"github.com/gofiber/fiber/v3"
)

type DataController struct {
	service *services.DataService
}

func NewDataController(service *services.DataService) *DataController {
	return &DataController{service: service}
}

func (dt *DataController) GetInformsRecord(c fiber.Ctx) error {
	site := c.Query("site")
	startDatestr := c.Query("startDatestr")
	endDatesrt := c.Query("endDatesrt")
	academicProgram := c.Query("academicProgram")
	documentNumber := c.Query("documentNumber")
	dependency := c.Query("dependency")
	reason := c.Query("reason")
	var startDate, endDate *time.Time
	var err error

	if startDatestr != "" {
		parsedStartDate, err := time.Parse("2006-01-02", startDatestr)
		if err != nil {
			return c.Status(400).JSON(fiber.Map{
				"error": "error al parsear fecha de inicio",
			})
		}
		startDate = &parsedStartDate
	}

	if endDatesrt != "" {
		parsedEndDate, err := time.Parse("2006-01-02", endDatesrt)
		if err != nil {
			return c.Status(400).JSON(fiber.Map{
				"error": "error al parsear fecha de fin",
			})
		}
		endDate = &parsedEndDate
	}

	filters := utils.Filters{
		Site:            site,
		StartDate:       startDate,
		EndDate:         endDate,
		AcademicProgram: academicProgram,
		DocumentNumber:  documentNumber,
		Dependency:      dependency,
		Reason:          reason,
	}

	results, err := dt.service.GetInformation(filters)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	return c.Status(200).JSON(fiber.Map{"results": results})
}

func (dt *DataController) GetCombinedInformation(c fiber.Ctx) error {
	results, err := dt.service.GetCombinedData()
	if err != nil {
		log.Printf("error fetching combined data: %v", err)
		return c.Status(500).JSON(fiber.Map{
			"error": "Internal server error",
		})
	}

	return c.Status(200).JSON(results)
}

func (c *DataController) ExportXslx(ctx fiber.Ctx) error {

	file, err := c.service.ExportDataIngressRecord()
	if err != nil {
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": err.Error()})
	}
	log.Println("File created successfully")

	var buffer bytes.Buffer
	if err := file.Write(&buffer); err != nil {
		log.Println("Error writing file to buffer:", err)
		return ctx.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": err.Error(),
		})
	}

	downloadName := "clientes_" + time.Now().UTC().Format("2006-01-02") + ".xlsx"
	ctx.Set("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	ctx.Set("Content-Disposition", "attachment; filename="+downloadName)

	return ctx.SendStream(bytes.NewReader(buffer.Bytes()))

}

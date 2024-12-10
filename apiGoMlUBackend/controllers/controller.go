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

func (dt *DataController) GetUsers(c fiber.Ctx) error {
	users, err := dt.service.GetUsers()
	if err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{"error": "Failed to fetch users"})
	}
	return c.Status(fiber.StatusOK).JSON(users)
}

func (dt *DataController) GetInformsRecord(c fiber.Ctx) error {
	counterSitePrincipalstr := c.Query("sitePrincipal")
	counterSiteDowntownstr := c.Query("siteDowntown")
	counterTotalstr := c.Query("countTotal")
	loanBookstr := c.Query("loanBook")
	loanComputerstr := c.Query("loanComputer")
	consultRoomstr := c.Query("consultRoom")

	counterSiteDowntown, err := utils.ParseBoolParams(counterSiteDowntownstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}
	counterSitePrincipal, err := utils.ParseBoolParams(counterSitePrincipalstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}
	counterTotal, err := utils.ParseBoolParams(counterTotalstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}
	loanBook, err := utils.ParseBoolParams(loanBookstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}
	loanComputer, err := utils.ParseBoolParams(loanComputerstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}
	consultRoom, err := utils.ParseBoolParams(consultRoomstr)
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error": "error al parsear de string a bool",
		})
	}

	filters := utils.Filters{
		CounterSitePrincipal: counterSitePrincipal,
		CounterSiteDowntown:  counterSiteDowntown,
		CounterTotal:         counterTotal,
		LoanComputer:         loanComputer,
		LoanBook:             loanBook,
		ConsultRoom:          consultRoom,
	}

	results, err := dt.service.GetInformation(filters)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"error": "Error al obtener datos",
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

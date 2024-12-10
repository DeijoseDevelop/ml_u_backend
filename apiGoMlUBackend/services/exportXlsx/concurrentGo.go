package exportxlsx

import (
	"fmt"
	"log"
	"sync"
	"time"

	"github.com/Juan-Barraza/apiGoMl/utils"
	"github.com/xuri/excelize/v2"
)

func ProcessDataIngressRecordConcurrent(dataIngress []utils.IngressRecordData, file *excelize.File, selectedFields []string, sheetName string) error {
	datachan := make(chan utils.IngressRecordData)
	batchChan := make(chan []utils.IngressRecordData)
	var wg sync.WaitGroup

	location, err := time.LoadLocation("America/Bogota")
	if err != nil {
		log.Printf("Error al cargar la zona horaria de Bogotá: %v", err)
		return err
	}

	// Fase 1: Preparar los datos
	go func() {
		defer close(batchChan)
		batch := []utils.IngressRecordData{}
		for record := range datachan {
			batch = append(batch, record)
			if len(batch) >= BatchSize {
				batchChan <- batch
				batch = []utils.IngressRecordData{}
			}
		}
		if len(batch) > 0 {
			batchChan <- batch
		}
	}()

	// Fase 2: Procesar los datos concurrentemente
	for i := 0; i < MaxWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for batch := range batchChan {
				for rowIdx, dataRecord := range batch {
					rowIndex := rowIdx + 2 // Fila inicial para datos
					for colIndex, field := range selectedFields {
						cell := fmt.Sprintf("%s%d", string('A'+colIndex), rowIndex)
						value := ""
						timeStampColombia := dataRecord.TimeStamp.In(location)
						formattedTime := timeStampColombia.Format("2/01/2006 03:04:05 a. m.")
						switch field {
						case "TimeStamp":
							value = formattedTime
						case "DocumentNumber":
							value = dataRecord.DocumentNumber
						case "Gender":
							value = dataRecord.Gender
						case "UserType":
							value = dataRecord.UserType
						case "Dependency":
							value = dataRecord.Dependency
						case "AcademicProgram":
							value = dataRecord.AcademicProgram
						case "Reason":
							value = dataRecord.Reason
						}
						file.SetCellValue(sheetName, cell, value)
					}
				}
			}
		}(i)
	}

	for _, data := range dataIngress {
		datachan <- data
	}
	close(datachan)

	wg.Wait()
	
	return nil
}
